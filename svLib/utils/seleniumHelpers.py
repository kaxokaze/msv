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
    if options is None:
        chrome_options = ChromeOptions()
        # for headless chrome to load page with a normal speed, instead of like 2 mins per page
        # https://github.com/Codeception/CodeceptJS/issues/561#issuecomment-373666779
        if not uses_proxy:
            chrome_options.add_argument("--proxy-server='direct://'")
            chrome_options.add_argument("--proxy-bypass-list=*")
    else:
        chrome_options = options
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-extensions-file-access-check")
    chrome_options.add_argument("--disable-system-timezone-automatic-detection")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920x1100")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")

    if d_cap is None:
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
    d_cap['acceptSslCerts'] = True

    driver = selenium.webdriver.Chrome(executable_path=globalConstants.CHROMEDRIVER_PATH, chrome_options=chrome_options,
                                       desired_capabilities=d_cap)
    return driver


def createHeadlessFirefoxDriver(profile=None, proxy=None):
    options = FfOptions()
    options.add_argument("--headless")
    geckodriver = 'bin/geckodriver.exe'
    os.environ["webdriver.gecko.driver"] = geckodriver
    return selenium.webdriver.Firefox(firefox_options=options,
                                      executable_path=geckodriver,
                                      firefox_profile=profile,
                                      proxy=proxy)
