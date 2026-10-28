import re
import os
import threading
import zipfile
import platform
import subprocess

import requests
from bs4 import BeautifulSoup

from svLib.log import svLogger


def detect_architecture():
    _64_BIT = False
    WINDOWS = False
    bit, arch = platform.architecture()
    if bit == '64bit':
        _64_BIT = True
    if 'windows' in arch.lower():
        WINDOWS = True
        try:
            if os.environ['PROGRAMFILES'] == 'C:\\Program Files (x86)':
                _64_BIT = True
        except KeyError:
            pass
    return _64_BIT, WINDOWS


def identify_latest_version():
    r = requests.get("https://github.com/mozilla/geckodriver/releases")
    soup = BeautifulSoup(r.content, 'html.parser')
    span = soup.find(name='span', text='Latest')
    v_link = span.parent.parent.find("a")
    return v_link.text.strip()


def identify_geckodriver_url(_64_BIT, WINDOWS):
    ver = identify_latest_version()
    urls = {
        'linux32': f"https://github.com/mozilla/geckodriver/releases/download/v{ver}/geckodriver-v{ver}-linux32.tar.gz",
        'linux64': f'https://github.com/mozilla/geckodriver/releases/download/v{ver}/geckodriver-v{ver}-linux64.tar.gz',
        'win32': f'https://github.com/mozilla/geckodriver/releases/download/v{ver}/geckodriver-v{ver}-win32.zip',
        'win64': f'https://github.com/mozilla/geckodriver/releases/download/v{ver}/geckodriver-v{ver}-win64.zip'
    }
    if WINDOWS and _64_BIT:
        url = urls['win64']
    if WINDOWS and not _64_BIT:
        url = urls['win32']
    if not WINDOWS and _64_BIT:
        url = urls['linux64']
    if not WINDOWS and not _64_BIT:
        url = urls['linux32']
    return url


def get_current_chrome_version(WINDOWS):
    """Return the installed Chrome/Chromium version or raise a descriptive error."""
    if WINDOWS:
        command = [
            'reg', 'query',
            r'HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon',
            '/v', 'version'
        ]
    else:
        command = ['google-chrome', '--version']

    candidates = [command]
    if not WINDOWS:
        candidates.extend([
            ['chromium', '--version'],
            ['chromium-browser', '--version'],
            ['google-chrome-stable', '--version'],
        ])

    errors = []
    for candidate in candidates:
        try:
            result = subprocess.run(
                candidate,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                timeout=10,
                text=True,
            )
            match = re.search(r'\d+(?:\.\d+){2,3}', result.stdout)
            if match:
                return match.group(0)
            errors.append(f"{candidate[0]} did not report a version")
        except (OSError, subprocess.SubprocessError) as exc:
            errors.append(f"{candidate[0]}: {exc}")

    raise RuntimeError(
        "Could not detect an installed Chrome/Chromium version. "
        "Install a supported browser or configure its executable path. "
        + "; ".join(errors)
    )


def get_chrome_base_version(version):
    return version.split('.')[0]


def build_url(base_url, version, platform, architecture):
    url = base_url + version + '/chromedriver_' + platform + architecture + '.zip'
    return url


def is_valid_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return True
    return False


def parse_modern_matching_chromedriver_version_from_site(chrome_version, platform):
    url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()

        try:
            channels = data["channels"]
            version_prefix = ".".join(chrome_version.split(".")[:-1])
            for channel in channels.values():
                if channel["version"].startswith(version_prefix) and "chromedriver" in channel["downloads"]:
                    for driver_info in channel["downloads"]["chromedriver"]:
                        if driver_info["platform"] == platform:
                            return driver_info["url"]

            return None  # Chromedriver not found for the specified version and platform

        except KeyError:
            print("Invalid JSON data format.")
            return None

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None


def get_chromedriver_url(version, _64_BIT, WINDOWS):
    base_url = 'https://chromedriver.storage.googleapis.com/'
    if WINDOWS:
        platform = 'win'
        architecture = '32'  # only 32 bit is availiable for windows wtf.jpg
    else:
        platform = 'linux'
        architecture = '64'  # only 64 bit is availiable for linux wtf.jpg
    url = build_url(base_url, version, platform, architecture)
    if is_valid_url(url):
        return url
    s_version = parse_matching_chromedriver_version_from_site(version)
    if s_version is not None:
        url = build_url(base_url, s_version, platform, architecture)
    else:
        if _64_BIT:
            architecture = '64'
        else:
            architecture = '32'
        url = parse_modern_matching_chromedriver_version_from_site(version, platform+architecture)
    if is_valid_url(url):
        return url
    raise SystemExit("[!] ERROR: No valid chromedriver url avaliable")


def parse_matching_chromedriver_version_from_site(version):
    url = "https://chromedriver.chromium.org/downloads"
    base_version = get_chrome_base_version(version)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    all_urls = soup.find_all('a')
    for url in all_urls:
        try:
            if f"https://chromedriver.storage.googleapis.com/{base_version}" in url['href']:
                matching_version = re.findall(r"{}\.[0-9]+\.[0-9]+\.[0-9]+".format(base_version), url['href'])[0]
                return matching_version
        except KeyError:
            return None


def download_driver(url, driver_folder):
    if 'mozilla' in url:
        fname = "geckodriver.zip"
        svLogger.log_event(f"[+] Downloading geckodriver from: {url}")
    else:
        fname = "chromedriver.zip"
        svLogger.log_event(f"[+] Downloading chromedriver from: {url}")
    r = requests.get(url, stream=True)

    driver_path = os.path.join(driver_folder, fname)
    with open(driver_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)

    return driver_path


def unzip_archive(fname):
    svLogger.log_event(f'[+] Unzipping: {fname}')
    with zipfile.ZipFile(fname, 'r') as zip_ref:
        for member in zip_ref.namelist():
            if member.endswith('/'):
                continue  # Skip directories

            filename = os.path.basename(member)

            extracted_path = os.path.join(os.path.dirname(fname), filename)

            with zip_ref.open(member) as source, open(extracted_path, 'wb') as target:
                target.write(source.read())
    os.remove(fname)
    svLogger.log_event(f'[+] Done unzipping: {fname}. Updated.')


def get_geckodriver(driver_folder):
    # if 'geckodriver' in os.listdir() or 'geckodriver.exe' in os.listdir():
    #    return
    try:
        _64_BIT, WINDOWS = detect_architecture()

        url = identify_geckodriver_url(_64_BIT, WINDOWS)

        driver_path = download_driver(url, driver_folder)
        unzip_archive(driver_path)
    except Exception as e:
        svLogger.log_error("Failed to download geckodriver, error: ", e, ". Download it manually from https://github.com/mozilla/geckodriver/releases")


def get_chromedriver(driver_folder):
    # if 'chromedriver' in os.listdir() or 'chromedriver.exe' in os.listdir():
    #    return
    try:
        _64_BIT, WINDOWS = detect_architecture()

        version = get_current_chrome_version(WINDOWS)
        url = get_chromedriver_url(version, _64_BIT, WINDOWS)

        driver_path = download_driver(url, driver_folder)
        unzip_archive(driver_path)
    except Exception as e:
        svLogger.log_error("Failed to download chromedriver, error: ", e, ". Download it manually from https://sites.google.com/chromium.org/driver/")


def get_all_drivers(driver_folder):
    svLogger.log_event(f"[+] Beginning driver updates")

    get_chromedriver(driver_folder)
    get_geckodriver(driver_folder)

    if updates_finished_callback is not None:
        updates_finished_callback()


def start_updates_async(driver_folder):
    thread = threading.Thread(target=get_all_drivers, args=(driver_folder,))
    thread.start()


updates_finished_callback = None
