import os

import selenium
import selenium.webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FfOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from svLib.userData import svSettings
from svLib import globalConstants


def page_has_loaded(driver, old_page, old_url):
    try:
        new_page = driver.find_element_by_tag_name('html')
        return (new_page.id != old_page.id) or (driver.current_url != old_url)
    except NoSuchElementException:
        return False


def click_element(driver, element: WebElement):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

    try:
        WebDriverWait(driver, 1).until(expected_conditions.visibility_of(element))
    except:
        driver.execute_script("arguments[0].scrollIntoView(true);window.scrollBy(0,100);", element)
        try:
            WebDriverWait(driver, 1).until(expected_conditions.visibility_of(element))
        except:
            driver.execute_script("arguments[0].scrollIntoView(true);window.scrollBy(0,-100);", element)

    element.click()


def createPhantomJsDriver():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
    )
    service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false']
    return selenium.webdriver.PhantomJS("bin/phantomjs.exe", desired_capabilities=dcap, service_args=service_args,
                                               service_log_path=os.path.join(svSettings.program_data_folder, 'logs',
                                                                             'ghostdriver.log'))


def createHeadlessChromeDriver(d_cap=None, options=None, uses_proxy=False):
    chrome_options = options if options is not None else ChromeOptions()
    if options is None and not uses_proxy:
        # Bypass proxy configuration only for explicitly direct test sessions.
        chrome_options.add_argument("--proxy-server=direct://")
        chrome_options.add_argument("--proxy-bypass-list=*")

    for argument in (
        "--headless",
        "--mute-audio",
        "--ignore-certificate-errors",
        "--disable-extensions-file-access-check",
        "--disable-system-timezone-automatic-detection",
        "--disable-plugins-discovery",
        "--disable-extensions",
        "--window-size=1920x1100",
        "--dns-prefetch-disable",
        "--force-device-scale-factor=1",
        "--no-sandbox",
        "--disable-infobars",
        "--disable-dev-shm-usage",
        "--disable-browser-side-navigation",
        "--disable-gpu",
        "--autoplay-policy=no-user-gesture-required",
    ):
        chrome_options.add_argument(argument)

    # Copy desired capabilities before mutation so callers' shared defaults
    # cannot be changed as a side effect.
    capabilities = dict(DesiredCapabilities.CHROME if d_cap is None else d_cap)
    capabilities.setdefault("pageLoadStrategy", "eager")
    capabilities["acceptSslCerts"] = True

    return selenium.webdriver.Chrome(
        executable_path=globalConstants.CHROMEDRIVER_PATH,
        chrome_options=chrome_options,
        desired_capabilities=capabilities,
    )


def createHeadlessFirefoxDriver(profile=None, proxy=None):
    options = FfOptions()
    options.add_argument("--headless")
    geckodriver = 'bin/geckodriver.exe'
    os.environ["webdriver.gecko.driver"] = geckodriver
    return selenium.webdriver.Firefox(firefox_options=options,
                                      executable_path=geckodriver,
                                      firefox_profile=profile,
                                      proxy=proxy)
