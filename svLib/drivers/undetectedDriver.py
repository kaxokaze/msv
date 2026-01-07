import io
import os
import random
import re
import sys
import zipfile
from distutils.version import LooseVersion
from urllib.error import URLError
from urllib.request import urlopen, urlretrieve

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Chrome as _Chrome
from selenium.webdriver import ChromeOptions as _ChromeOptions
import svLib.drivers.driverUpdater

from svLib.log import svLogger
from svLib.system import childProcessesManager


logger = svLogger


TARGET_VERSION = 0


class Chrome:
    def __new__(cls, *args, enable_console_log=False, **kwargs):

        if not ChromeDriverManager.binary_patched:
            ChromeDriverManager(*args, **kwargs).install()
        if not ChromeDriverManager.selenium_patched:
            ChromeDriverManager(*args, **kwargs).patch_selenium_webdriver()
        if not kwargs.get("executable_path"):
            kwargs["executable_path"] = "./{}".format(
                ChromeDriverManager(*args, **kwargs).executable_path
            )
        if not kwargs.get("options"):
            kwargs["options"] = ChromeOptions()
        instance = object.__new__(_Chrome)

        try:
            instance.__init__(*args, **kwargs)
        except WebDriverException as e:
            if e.msg.startswith("unknown error: failed to wait for extension background page to load:"):
                pid = instance.service.process.pid
                childProcessesManager.purge_children(pid=pid, separate_thread=False)
            instance.quit()
            raise
        except Exception:
            instance.quit()
            raise

        instance._orig_get = instance.get

        def _get_wrapped(*args, **kwargs):
            if instance.execute_script("return navigator.webdriver"):
                instance.execute_cdp_cmd(
                    "Page.addScriptToEvaluateOnNewDocument",
                    {
                        "source": """

                            Object.defineProperty(window, 'navigator', {
                                value: new Proxy(navigator, {
                                has: (target, key) => (key === 'webdriver' ? false : key in target),
                                get: (target, key) =>
                                    key === 'webdriver'
                                    ? undefined
                                    : typeof target[key] === 'function'
                                    ? target[key].bind(target)
                                    : target[key]
                                })
                            });
                        """
                        + (
                            "console.log = console.dir = console.error = function(){};"
                            if not enable_console_log
                            else ""
                        )
                    },
                )
            return instance._orig_get(*args, **kwargs)

        instance.get = _get_wrapped

        original_user_agent_string = instance.execute_script(
            "return navigator.userAgent"
        )
        instance.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {"userAgent": original_user_agent_string.replace("Headless", ""),},
        )
        logger.log_event(f"[undetectable_driver] starting undetectable chromedriver Chrome({args}, {kwargs})")
        return instance


class ChromeOptions:
    def __new__(cls, *args, **kwargs):
        if not ChromeDriverManager.binary_patched:
            ChromeDriverManager(*args, **kwargs).install()
        if not ChromeDriverManager.selenium_patched:
            ChromeDriverManager(*args, **kwargs).patch_selenium_webdriver()

        instance = object.__new__(_ChromeOptions)
        instance.__init__()
        instance.add_argument("start-maximized")
        instance.add_experimental_option("excludeSwitches", ["enable-automation"])
        instance.add_argument("--disable-blink-features=AutomationControlled")
        return instance


class ChromeDriverManager(object):

    binary_patched = False
    selenium_patched = False
    target_version = None

    DL_BASE = "https://chromedriver.storage.googleapis.com/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):

        _platform = sys.platform

        if TARGET_VERSION:
            # use global if set
            self.target_version = TARGET_VERSION

        if target_version:
            # use explicitly passed target
            self.target_version = target_version  # user override

        if not self.target_version:
            # none of the above (default) and just get current version
            try:
                self.target_version = self.get_release_version_number().version[
                    0
                ]  # only major version int
            except URLError as e:
                _, is_windows = svLib.drivers.driverUpdater.detect_architecture()
                self.target_version = svLib.drivers.driverUpdater.get_chrome_base_version(
                    svLib.drivers.driverUpdater.get_current_chrome_version(is_windows))

        self._base = base_ = "chromedriver{}"

        exe_name = self._base
        if _platform in ("win32",):
            exe_name = base_.format(".exe")
        if _platform in ("linux",):
            _platform += "64"
            exe_name = exe_name.format("")
        if _platform in ("darwin",):
            _platform = "mac64"
            exe_name = exe_name.format("")
        self.platform = _platform
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

    def patch_selenium_webdriver(self):
        """
        Patches selenium package Chrome, ChromeOptions classes for current session

        :return:
        """
        import selenium.webdriver

        selenium.webdriver.Chrome = Chrome
        selenium.webdriver.ChromeOptions = ChromeOptions
        logger.log_event("[undetectable_driver] Selenium patched. Safe to import Chrome / ChromeOptions")
        ChromeDriverManager.selenium_patched = True

    def install(self, patch_selenium=True):
        """
        Initialize the patch

        This will:
         download chromedriver if not present
         patch the downloaded chromedriver
         patch selenium package if <patch_selenium> is True (default)

        :param patch_selenium: patch selenium webdriver classes for Chrome and ChromeDriver (for current python session)
        :return:
        """
        if not os.path.exists(self.executable_path):
            self.fetch_chromedriver()

        if not ChromeDriverManager.binary_patched:
            self.patch_binary()
            ChromeDriverManager.binary_patched = True

        if patch_selenium:
            self.patch_selenium_webdriver()

    def get_release_version_number(self):
        """
        Gets the latest major version available, or the latest major version of self.target_version if set explicitly.

        :return: version string
        """
        path = (
            "LATEST_RELEASE"
            if not self.target_version
            else f"LATEST_RELEASE_{self.target_version}"
        )
        return LooseVersion(urlopen(ChromeDriverManager.DL_BASE + path).read().decode())

    def fetch_chromedriver(self):
        """
        Downloads ChromeDriver from source and unpacks the executable

        :return: on success, name of the unpacked executable
        """
        base_ = self._base
        zip_name = base_.format(".zip")
        ver = self.get_release_version_number().vstring
        if os.path.exists(self.executable_path):
            return self.executable_path
        urlretrieve(
            f"{ChromeDriverManager.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip",
            filename=zip_name,
        )
        with zipfile.ZipFile(zip_name) as zf:
            zf.extract(self._exe_name)
        os.remove(zip_name)
        if sys.platform != "win32":
            os.chmod(self._exe_name, 0o755)
        return self._exe_name

    def patch_binary(self):
        """
        Patches the ChromeDriver binary

        :return: False on failure, binary name on success
        """
        linect = 0
        with io.open(self.executable_path, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"cdc_" in line:
                    fh.seek(-len(line), 1)
                    newline = re.sub(b"cdc_.{22}", self.get_random_bin_string(26), line)
                    fh.write(newline)
                    linect += 1
            return linect

    def get_random_bin_string(self, length):
        string = ""
        for i in range(length):
            string += chr(random.randint(97,122))
        return string.encode()


def install(executable_path=None, target_version=None, patch_selenium=True, *args, **kwargs):
    ChromeDriverManager(executable_path, target_version, *args, **kwargs).install(patch_selenium)
