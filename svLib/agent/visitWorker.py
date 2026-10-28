import datetime
import math
import os
import random
import re
import threading
import time
import weakref
import json
from urllib.parse import urlparse
from contextlib import contextmanager

from selenium import webdriver

from selenium.common.exceptions import TimeoutException, WebDriverException, ElementNotInteractableException, \
    ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from svLib import globalConstants
from svLib.agent import AgentModel
from svLib.exceptions.chrome_page_exception import ChromePageException
from svLib.log import svLogger
from svLib.userData import svSettings
from svLib.utils import seleniumHelpers, chromeProxyAuth, stdHelper


##########################################
# This class is responsible for creating an independent worker thread, that does the page visiting with
# some proxy, referral, user agent, etc.
##########################################
class VisitWorker:
    ALL_LINKS = 1
    INTERNAL_LINKS = 2
    EXTERNAL_LINKS = 3
    AUTO_RANDOM_ALLOWED_LINKS_TYPES = {
        ALL_LINKS: globalConstants.AUTO_RANDOM_ANY_LINKS,
        INTERNAL_LINKS: globalConstants.AUTO_RANDOM_INTERNAL_LINKS,
        EXTERNAL_LINKS: globalConstants.AUTO_RANDOM_EXTERNAL_LINKS
    }

    @staticmethod
    def get_link_types():
        return list(VisitWorker.AUTO_RANDOM_ALLOWED_LINKS_TYPES.values())

    def __init__(self, agent_settings, scheduler, website, referrer, user_agent, proxy_string,
                 browser=globalConstants.BR_FX):
        self.agent_settings: AgentModel = agent_settings

        self.thread = None
        self.driver = None

        self.website = website
        self.referrer = referrer
        self.user_agent = user_agent
        self.proxy_string = proxy_string
        self.browser_type = browser

        self.alive = True
        self.scheduler = weakref.ref(scheduler)

        self.proxy_plugin_path = None

    def start(self):
        if not self.alive:
            return

        self.scheduler().add_worker(self)
        self.scheduler().thread_pool.queueTask(self.visit_page)

    def visit_page(self):
        self.thread = threading.current_thread()
        if not self.alive:
            return

        # get the parsed parameters for the proxy
        proxy_addr = proxy_type = user_name = password = None
        if self.proxy_string is not None and self.proxy_string != '':
            proxy_addr, proxy_type, user_name, password = self.parse_proxy_str(self.proxy_string)

        # configure the browser, stop visitor in case of an error
        if not self.create_webdriver(proxy_addr, proxy_type, user_name, password):
            return

        # work might have been interrupted from some other thread,
        # so check for it before we attempt any loading
        if not self.alive:
            try:
                self.driver.quit()
            except:
                pass
            self.join()
            return

        # Try loading the target page
        try:
            # random window dimensions, we can set 'em once we have the driver object
            w_dim = self.agent_settings.sva_window_dims[random.randint(0, len(self.agent_settings.sva_window_dims) - 1)]
            self.driver.set_window_size(w_dim[0], w_dim[1])

            self.preload_cookies_file(self.website)

            # get to the target page through a modified referrer page
            if self.agent_settings.sva_use_js_ref and self.referrer is not None and self.referrer != '':
                self.set_wait_interval(self.agent_settings.sva_js_inject_timeout)

                try:
                    self.driver.get(self.referrer)
                except:
                    pass

                script_text = """
                    window.stop();

                    document.body.innerHTML = '<a href="%s">MassSiteVisitorInternalRedirectLink</a>';
                """ % self.website

                self.driver.execute_script(script_text)
                svLogger.log_event("After loading ref page, injected the target link", self.driver.page_source[-150:],
                                   self.driver.current_url, len(self.driver.page_source))

                # constrain the loading time for the page
                self.set_wait_interval(self.agent_settings.sva_timeout_interval)

                if self.browser_type != globalConstants.BR_FX:
                    seleniumHelpers.click_element(self.driver, self.driver.find_element_by_link_text(
                        'MassSiteVisitorInternalRedirectLink'))
                else:
                    with self.wait_for_page_load(self.agent_settings.sva_timeout_interval):
                        seleniumHelpers.click_element(self.driver, self.driver.find_element_by_link_text(
                            'MassSiteVisitorInternalRedirectLink'))
            else:
                # just normally get the page, referrer will only be set in http headers, not available in the js DOM
                # (like for goog analytics)
                # constrain the loading time for the page
                self.set_wait_interval(self.agent_settings.sva_timeout_interval)

                self.driver.get(self.website)

            if self.browser_type == globalConstants.BR_CHR:
                self.check_chrome_response_page()
        except TimeoutException as e:  # catch target page loading failure (timeout)
            self.check_response_success_and_log(0, self.proxy_string)  # make sure we mark the failure to respond

            svLogger.log_error('Loading the page', self.website, 'from proxy', self.proxy_string, 'timed out.')
            self.scheduler().countTimeout()
        except (WebDriverException, ChromePageException) as e:  # catch the general selenium page loading exceptions
            self.check_response_success_and_log(0, self.proxy_string)  # make sure we mark the failure to respond

            svLogger.log_error('Loading the page', self.website, 'from proxy', self.proxy_string, 'failed.', e)
            self.scheduler().countError()
        except Exception as e:  # catch target page loading failures (something general, unpredicted, fuck it)
            # TODO: handle when a browser error page is displayed
            svLogger.log_error('Loading the page', self.website, 'from proxy', self.proxy_string, 'failed.', e)
            self.scheduler().countError()
        else:  # Loading the target page didn't fail, do our thing
            # record the current response
            try:
                bytes_received = len(self.driver.page_source)
            except:
                bytes_received = 0
            try:
                svLogger.log_event('Got a response from', self.proxy_string, 'for', self.website, 'size', bytes_received)
                if self.check_response_success_and_log(bytes_received, self.proxy_string):
                    # screen before the user action
                    self.save_snapshot()

                    # Wait as defined in options
                    self.wait_time(
                        random.uniform(self.agent_settings.sva_min_page_time, self.agent_settings.sva_max_page_time))

                    # scripted behaviour, if defined by the user
                    if self.perform_scripted_behavior():
                        svLogger.log_event('Successful script execution on page', self.website)

                        self.wait_time(self.agent_settings.sva_after_script_time)

                        # screencap after the user action
                        self.save_snapshot('AFTER_SCRIPT')

                    self.execute_autorandom_logic()
            except Exception as e:
                svLogger.log_error('Performing after-loading logic for page', self.website, 'from proxy', self.proxy_string, 'failed.', e)
        finally:
            # quit the driver, after all work is done
            try:
                self.driver.quit()
            except:
                pass

            # clear the worker from the list
            self.join()

    def start_test(self):
        if not self.alive:
            return

        self.scheduler().add_worker(self)
        self.scheduler().thread_pool.queueTask(self.test_proxy)

    # This will perform a test request to the proxy, several times, or until a
    # proper response is received
    def test_proxy(self):
        self.thread = threading.current_thread()
        if not self.alive:
            return

        proxy_addr, proxy_type, username, password = self.parse_proxy_str(self.proxy_string)

        svLogger.log_event('Testing proxy', self.proxy_string, 'with url', self.website)

        try:
            options = webdriver.ChromeOptions()
            capabilities = dict(DesiredCapabilities.CHROME)

            if proxy_type is not None:  # socks 4/5 proxy
                proxy_arg = ("--proxy-server=%s://" % proxy_type) + proxy_addr
                options.add_argument(proxy_arg)
            else:  # http proxy
                capabilities['proxy'] = {
                    'httpProxy': proxy_addr,
                    'sslProxy': proxy_addr,
                    'proxyType': "MANUAL",
                    'autodetect': False,
                    'noProxy': None,
                }

            self.driver = seleniumHelpers.createHeadlessChromeDriver(capabilities, options, True)
        except Exception as e:
            try:
                profile = webdriver.FirefoxProfile()

                self.set_up_ff_proxy(proxy_addr, proxy_type, profile)

                self.driver = seleniumHelpers.createHeadlessFirefoxDriver(profile)
            except Exception as e:
                svLogger.log_error("Testing proxy failed, couldn't start a driver", e)
                return

        if not self.alive:
            self.driver.quit()
            return

        # several attempts (as defined in options) with timeout, in one thread with one driver object
        test_attempts = 0
        successful_attempt = False
        while (not successful_attempt) and test_attempts <= self.agent_settings.sva_max_proxy_fails and self.alive:
            test_attempts += 1

            try:
                self.set_wait_interval(self.agent_settings.sva_timeout_interval)

                self.driver.get(self.website)
            except TimeoutException as e:  # catch loading failures
                self.check_response_success_and_log(0, self.proxy_string)  # make sure we mark the failure to respond
                svLogger.log_error('Testing the proxy', self.proxy_string, 'with page', self.website, 'timed out.')
                self.scheduler().countTimeout()
            except WebDriverException as e:
                proxy_connection_errors = ['net::ERR_PROXY_CONNECTION_FAILED',
                                           'net::ERR_CONNECTION_RESET',
                                           'net::ERR_TUNNEL_CONNECTION_FAILED']
                if any(substring in e.msg for substring in proxy_connection_errors):
                    self.check_response_success_and_log(0, self.proxy_string)  # make sure we mark the failure to respond
                    svLogger.log_error('Testing the proxy', self.proxy_string, 'with page', self.website, 'timed out: ', e)
                    self.scheduler().countTimeout()
            except Exception as e:
                svLogger.log_error('Testing the proxy', self.proxy_string, 'with page', self.website, 'failed.', e)
                self.scheduler().countError()
            else:  # loading didn't fail, do our thing
                # record the current response
                try:
                    bytes_received = len(self.driver.page_source)
                except:
                    bytes_received = 0
                svLogger.log_event('Got a response from', self.proxy_string, 'for', self.website, 'size',
                                   bytes_received)

                successful_attempt = self.check_response_success_and_log(bytes_received, self.proxy_string)

            time.sleep(3.)

        # quit the driver
        self.driver.quit()

        # clear the thread from the list
        self.join()

    def create_webdriver(self, proxy_addr, proxy_type, user_name, password):
        try:
            if self.browser_type == globalConstants.BR_PJS:
                self.setup_phantomjs(self.agent_settings.sva_browser_paths[self.browser_type], self.referrer,
                                     self.user_agent, proxy_addr,
                                     proxy_type, user_name, password)
            elif self.browser_type == globalConstants.BR_FX:

                self.setup_firefox(self.agent_settings.sva_browser_paths[self.browser_type], self.referrer,
                                   self.user_agent, proxy_addr,
                                   proxy_type, user_name, password)
            elif self.browser_type == globalConstants.BR_CHR:
                self.setup_chrome(self.agent_settings.sva_browser_paths[self.browser_type], self.referrer,
                                  self.user_agent, proxy_addr,
                                  proxy_type, user_name, password)
            else:
                svLogger.log_error('Unsupported browser type:', self.browser_type)
                self.join()
                return
        except Exception as e:  # failed to create a driver, kill everything
            svLogger.log_error('Error launching a', self.browser_type, 'browser.', e)

            try:
                self.driver.quit()
            except:
                pass

            self.join()
            return False
        else:
            return True

    def setup_chrome(self, browser_path, referrer, user_agent, proxy_addr, proxy_type, usrname, password):
        options = webdriver.ChromeOptions()
        capabilities = dict(DesiredCapabilities.CHROME)

        proxy_available = proxy_addr is not None

        if self.agent_settings.sva_headless_mode:
            options.add_argument("--headless")
            if not proxy_available:
                # for headless chrome to load page with a normal speed, instead of like 2 mins per page
                # https://github.com/Codeception/CodeceptJS/issues/561#issuecomment-373666779
                options.add_argument("--proxy-server='direct://'")
                options.add_argument("--proxy-bypass-list=*")

        if not self.agent_settings.images_enabled:
            options.add_argument('--blink-settings=imagesEnabled=false')

        if usrname is not None and password is not None:
            pr_parts = proxy_addr.split(':')

            proxy_scheme = proxy_type
            if proxy_type is None:
                proxy_scheme = "http"
            time_stamp = str(datetime.datetime.now().time()).replace(':', "-")
            self.proxy_plugin_path = os.path.join(svSettings.program_data_folder,
                                                  'chrproxplug' + proxy_addr.replace(':', '-') + time_stamp + '.zip')
            chromeProxyAuth.createAddonFile(pr_parts[0], pr_parts[1], usrname, password, proxy_scheme,
                                            self.proxy_plugin_path)
            options.add_extension(self.proxy_plugin_path)
        else:
            if proxy_available:
                if proxy_type is not None:  # socks 4/5 proxy
                    proxy_arg = ("--proxy-server=%s://" % proxy_type) + proxy_addr
                    options.add_argument(proxy_arg)
                else:  # http proxy
                    capabilities['proxy'] = {
                        'httpProxy': proxy_addr,
                        'sslProxy': proxy_addr,
                        'proxyType': "MANUAL",
                        'autodetect': False,
                        'noProxy': None,
                    }
        options.add_argument("--mute-audio")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions-file-access-check")
        options.add_argument("--disable-system-timezone-automatic-detection")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--autoplay-policy=no-user-gesture-required")

        if self.agent_settings.sva_hide_offscreen:
            options.add_argument("--window-position=-2000,-10000")
        if user_agent is not None and user_agent != '':
            options.add_argument('--user-agent=' + user_agent)

        if self.agent_settings.sva_timeout_interval:
            locale = self.choose_random_locale()
            if locale:
                options.add_argument("--lang=" + locale)
                options.add_experimental_option('prefs', {'intl.accept_languages': locale})

        if self.agent_settings.sva_alexa_enabled:
            options.add_extension('bin/alexabar.crx')

        if self.agent_settings.enable_similarweb:
            options.add_extension('bin/similarweb_6_8_1_0.crx')

        if browser_path != '':
            capabilities['chrome.binary'] = browser_path
            options.binary_location = browser_path

        # driver is created here
        try:
            self.agent_settings.chrome_start_semaphore.acquire()
            if self.alive:
                self.driver = webdriver.Chrome(executable_path=globalConstants.CHROMEDRIVER_PATH,
                                               desired_capabilities=capabilities, chrome_options=options)
        except Exception as e:
            raise e
        finally:
            self.agent_settings.chrome_start_semaphore.release()

        if self.alive and self.agent_settings.sva_hide_offscreen:
            self.driver.set_window_position(-2000, -10000)

        if self.alive:
            if self.agent_settings.sva_alexa_enabled:
                try:
                    time.sleep(1.0)
                    self.driver.get('chrome-extension://cknebhggccemgcnbidipinkifmmegdel/html/welcome.html')
                    self.driver.execute_script(""" localStorage.setItem('privacyPolicyAccepted', 'true'); """)
                except Exception as e:
                    svLogger.log_error("Failed to configure the Alexa extension ", e)
            if self.agent_settings.enable_similarweb:
                try:
                    time.sleep(1.0)
                    self.driver.get(self.agent_settings.similarweb_ex_path)
                    WebDriverWait(self.driver, 5).until(
                        expected_conditions.presence_of_element_located((By.XPATH, "//button[text()='Yes']"))
                    ).click()
                except Exception as e:
                    svLogger.log_error("Failed to configure the sIMILARWEB extension ", e)

    def setup_firefox(self, browser_path, referrer, user_agent, proxy_addr, proxy_type, username, password):
        profile = webdriver.FirefoxProfile()
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_options = FirefoxOptions()

        if self.agent_settings.sva_headless_mode:
            firefox_options.add_argument("--headless")

        if not self.agent_settings.images_enabled:
            profile.set_preference('permissions.default.image', 2)

        self.set_up_ff_proxy(proxy_addr, proxy_type, profile)

        profile.set_preference("media.volume_scale", "0.0")
        profile.set_preference("extensions.legacy.enabled", "true")
        profile.set_preference("xpinstall.signatures.required", "false")
        profile.set_preference("xpinstall.whitelist.required", "false")
        profile.set_preference("privacy.trackingprotection.enabled", "true")
        profile.set_preference("privacy.trackingprotection.fingerprinting.enabled", "true")
        profile.set_preference("privacy.trackingprotection.pbmode.enabled", "true")
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference("useAutomationExtension", False)
        profile.DEFAULT_PREFERENCES['frozen']["extensions.legacy.enabled"] = True

        if user_agent is not None and user_agent != '':
            profile.set_preference("general.useragent.override", user_agent)

        firefox_capabilities['marionette'] = True
        firefox_capabilities['firefox_profile'] = profile.encoded
        firefox_binary = None
        if browser_path != '':
            firefox_binary = FirefoxBinary(browser_path)

        # this will be used to select geckodriver properly
        geckodriver = 'bin/geckodriver.exe'

        os.environ["webdriver.gecko.driver"] = geckodriver

        if self.agent_settings.sva_timeout_interval:
            locale = self.choose_random_locale()
            if locale:
                profile.set_preference("intl.accept_languages", locale)

        # create the driver
        try:
            self.agent_settings.firefox_start_semaphore.acquire()
            if self.alive:
                self.driver = webdriver.Firefox(executable_path=geckodriver, firefox_profile=profile,
                                                capabilities=firefox_capabilities,
                                                firefox_options=firefox_options, firefox_binary=firefox_binary,
                                                log_path=os.path.join(svSettings.program_data_folder, 'logs',
                                                                      'geckodriver.log'))
        except Exception as e:
            raise e
        finally:
            self.agent_settings.firefox_start_semaphore.release()

        if self.alive and self.agent_settings.sva_alexa_enabled:
            alexa_addon_abs_path = os.path.join(os.getcwd(), 'bin', 'alexabar_ff.xpi')
            self.driver.install_addon(alexa_addon_abs_path)

        if self.alive and self.agent_settings.enable_similarweb:
            addon_abs_path = os.path.join(os.getcwd(), 'bin', 'similarweb_5.5.7.xpi')
            self.driver.install_addon(addon_abs_path)

        if self.alive and self.agent_settings.sva_hide_offscreen:
            self.driver.set_window_position(20000, 10000)

    def set_up_ff_proxy(self, proxy_addr, proxy_type, profile):
        if proxy_addr is not None:
            profile.set_preference('network.proxy.type', 1)  # manual proxy

            proxy_ip = proxy_addr.split(":")[0]
            proxy_port = proxy_addr.split(":")[1]
            if proxy_type is None:
                profile.set_preference("network.proxy.http", proxy_ip)
                profile.set_preference("network.proxy.http_port", int(proxy_port))
                profile.set_preference("network.proxy.ssl", proxy_ip)
                profile.set_preference("network.proxy.ssl_port", int(proxy_port))
            else:
                profile.set_preference('network.proxy.socks', proxy_ip)
                profile.set_preference('network.proxy.socks_port', int(proxy_port))
                profile.set_preference('network.proxy.socks_version', int(proxy_type[-1]))
                profile.set_preference('network.proxy.socks_remote_dns', True)

    def setup_phantomjs(self, browser_path, referrer, user_agent, proxy_addr, proxy_type, user_name, password):
        # use agent and referrer is in the desired capabilities
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        if referrer is not None and referrer != '':
            dcap["phantomjs.page.customHeaders.Referer"] = (referrer)
            dcap["phantomjs.page.customHeaders.Upgrade-Insecure-Requests"] = ('1')
        if self.agent_settings.sva_timeout_interval:
            locale = self.choose_random_locale()
            dcap["phantomjs.page.customHeaders.Accept-Language"] = locale
        if user_agent is not None and user_agent != '':
            dcap["phantomjs.page.settings.userAgent"] = (user_agent)

        service_args = ['--config=cfg/phantomjs_config.json']

        if not self.agent_settings.images_enabled:
            service_args.append('--load-images=no')
        else:
            service_args.append('--load-images=yes')

        if proxy_addr is not None:
            service_args.append('--proxy=' + proxy_addr)
        if proxy_type is not None:
            service_args.append('--proxy-type=' + proxy_type)
        if user_name is not None and password is not None:
            service_args.append('--proxy-auth=' + user_name + ':' + password)

        self.driver = webdriver.PhantomJS(browser_path, desired_capabilities=dcap, service_args=service_args,
                                          service_log_path=os.path.join(svSettings.program_data_folder, 'logs',
                                                                        'ghostdriver.log'))

    # Will append the parsed proxy data, if the service args aray is provided
    def parse_proxy_str(self, proxy_string):
        proxy_addr = proxy_type = username = password = None

        try:
            proxy_addr = re.findall(r'(?:[A-Za-z0-9-]+\.)+[A-Za-z0-9]{1,3}:\d{1,6}', proxy_string)[0]
        except Exception as e:
            svLogger.log_error('Proxy string', proxy_string,
                               "is incorrect, no IP found, format: 127.0.0.1:8080 socks5 u:username p:password, with 127.0.0.1:8080 the only mandatory part",
                               e)
        else:
            proxy_type_scanned = re.findall(r'\S+', proxy_string)
            for substring in proxy_type_scanned:
                if not stdHelper.isProxyString(substring):
                    prefix = substring[0:2]
                    if 'u:' == prefix:
                        username = substring[2:]
                    elif 'p:' == prefix:
                        password = substring[2:]
                    else:
                        proxy_type = substring

        return proxy_addr, proxy_type, username, password

    # trows exception in case there's something wrong with the currently loaded page (like we got a browser error page)
    def check_chrome_response_page(self):
        # will throw selenium.common.exceptions.NoSuchElementException if html element not located,
        # and that can only mean one thing - some kind of failure to load

        self.set_wait_interval(5)

        root_html = self.driver.find_element_by_xpath("//html")

        try:
            main_error_div = root_html.find_element_by_xpath("//div[@id='main-frame-error'][@class='interstitial-wrapper']")
            error_type_div = main_error_div.find_element_by_xpath("//div[@jscontent='errorCode'][@class='error-code']")
            print(error_type_div)
        except TimeoutException as e:
            if "Timed out receiving message from renderer" in e.msg:
                raise ChromePageException('Probably a chrome error page')
        except Exception as e:
            pass  # no error elements, continue normally
        else:
            raise ChromePageException('Probably a chrome error page')  # chrome error element found, throw an exception
        finally:
            self.set_wait_interval(self.agent_settings.sva_timeout_interval)

    # Is necessary, because firefox returns prematurely after click(),
    # doesn't even consider waiting for page to load, like in case of get()
    @contextmanager
    def wait_for_page_load(self, timeout):
        old_page = self.driver.find_element_by_tag_name('html')

        yield

        # first we wait for html root tag to change (means we're on a new page)
        WebDriverWait(self.driver, timeout).until(
            expected_conditions.staleness_of(old_page)
        )

        # and now we assume that any real web-page will have some link on it,
        # so we wait for at least any link to became clickable
        # Note: still it's beter to wait some time manually with timer, especially with proxies
        # because return from here will still be somewhat premature
        WebDriverWait(self.driver, timeout).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//a"))
        )

    def wait_time(self, time_float_s):
        for j in range(int(math.ceil(time_float_s))):
            if not self.alive:
                return

            time_left = time_float_s - j
            time.sleep(max(0., min(0.1, time_left)))

    def save_snapshot(self, filename_postfix: str = ""):
        # if the option is set, save snapshot of the page as seen by the browser
        file_path: str = str()
        if self.agent_settings.sva_do_snapshots and self.alive:
            try:
                filename = self.website[:40].replace(':', '').replace('/', '-').replace('?', '-').replace('&',
                                                                                                          '-').replace(
                    '=', '-') + \
                           '_' + (self.proxy_string.replace(':',
                                                            ' ') if self.proxy_string is not None else globalConstants.TXT_NOPROXY) + '_' + \
                           str(datetime.datetime.now().time()).replace(':', "-") + filename_postfix
                file_path = os.path.join(svSettings.program_data_folder, 'visits', filename)
                # FileHelper.savePage( filename + '.html', self.driver.page_source.encode('utf-8') )
                self.driver.save_screenshot(file_path + '.png')
            except Exception as e:
                self.scheduler().countError()
                svLogger.log_error('Saving a screenshot to the file', file_path, 'failed:\n' + str(e))

    def check_response_success_and_log(self, bytes_received, proxy_string):
        if not self.alive:
            return False

        # Serialize updates to per-proxy statistics. Always release the semaphore,
        # even if a logger or callback unexpectedly raises.
        stat_sem = self.scheduler().get_sv_stat_log_sem()
        stat_sem.acquire()
        try:
            is_success = bytes_received > self.agent_settings.sva_success_page_min_size
            if is_success:
                self.scheduler().countSuccess()
            else:
                self.scheduler().countError()
                svLogger.log_error(
                    'Response size from proxy', proxy_string, 'has size', bytes_received,
                    'which is less than the size of a minimal correct response',
                    self.agent_settings.sva_success_page_min_size
                )

            entry = proxy_string if proxy_string is not None else globalConstants.TXT_NOPROXY
            responses = self.agent_settings.sv_proxy_responses.setdefault(entry, [])
            responses.append(bytes_received)

            # Notify UI callbacks only when configured. A missing optional callback
            # must not turn a completed request into an unhandled worker failure.
            if entry != globalConstants.TXT_NOPROXY:
                if is_success:
                    callback = self.agent_settings.sv_proxy_success_callback
                else:
                    callback = self.agent_settings.sv_proxy_fail_callback
                if callback is not None:
                    callback(proxy_string)

            return is_success
        finally:
            stat_sem.release()

    def perform_scripted_behavior(self):
        script_executed = False

        for us_script in self.agent_settings.sva_user_scripts:
            if not self.alive:
                return False

            script_on = us_script[0]  # on
            script_website = us_script[1]  # website
            script_el_name = us_script[2]  # el name
            script_attr_name = us_script[3]  # attr name
            script_search_type = us_script[4]  # search_type
            script_value = us_script[5]  # search val

            try:
                script_chance = int(us_script[6])  # percent
            except Exception as e:
                svLogger.log_error("incorrect chance value", us_script[6], e)
                continue

            iframe_type = us_script[7]
            iframe_value = us_script[8]

            self.driver.implicitly_wait(5)

            if script_on and script_website in self.driver.current_url:
                svLogger.log_event('Found a script for the page', script_website, "while at url",
                                   self.driver.current_url, "executing...")

                rolled_chance = random.randint(1, 100)

                if rolled_chance > min(100, max(1, script_chance)):
                    svLogger.log_event("We rolled", rolled_chance, 'which is more than a chance value', script_chance,
                                       'so we skip the script this time')
                    continue

                # in case element is in some inner iframe, switch the context
                if iframe_type != globalConstants.NO_IFRAME:
                    try:
                        iframe = self.driver.find_element_by_xpath(
                            "//iframe[@" + iframe_type + "='" + iframe_value + "']"
                        )
                        self.driver.switch_to.frame(frame_reference=iframe)
                    except Exception as e:
                        svLogger.log_error('Failed to find iframe with attribute', iframe_type, " = ", iframe_value,
                                           ": ", e)
                        self.driver.switch_to.default_content()
                        continue

                # now seek out the actual clickable element
                found_element = None
                if script_search_type == globalConstants.TXT_CONTAINS:
                    try:
                        if script_attr_name == globalConstants.TXT_SEARCH_BY_TEXT:
                            found_element = self.driver.find_element_by_xpath(
                                "//" + script_el_name + "[contains(text(), '" + script_value + "')]"
                            )
                        else:
                            found_element = self.driver.find_element_by_xpath(
                                "//" + script_el_name + "[contains(normalize-space(@" + script_attr_name + "), '" + script_value + "')]"
                            )
                    except Exception as e:
                        svLogger.log_error("failed to click the element", script_el_name, "with attribute",
                                           script_attr_name, script_value, e)
                        self.driver.switch_to.default_content()
                        continue
                elif script_search_type == globalConstants.TXT_EQUALS:
                    try:
                        if script_attr_name == globalConstants.TXT_SEARCH_BY_TEXT:
                            found_element = self.driver.find_element_by_xpath(
                                "//" + script_el_name + "[text() ='" + script_value + "']"
                            )
                        else:
                            found_element = self.driver.find_element_by_xpath(
                                "//" + script_el_name + "[@" + script_attr_name + "='" + script_value + "']"
                            )
                    except Exception as e:
                        svLogger.log_error("failed to click the element", script_el_name, "with attribute",
                                           script_attr_name, script_value, e)
                        self.driver.switch_to.default_content()
                        continue

                if found_element is not None:
                    self.set_wait_interval(self.agent_settings.sva_timeout_interval)
                    # it can actually fail, if the element's 'visible' is False
                    try:
                        seleniumHelpers.click_element(self.driver, found_element)
                    except Exception as e:
                        svLogger.log_error("exception during the click on", script_el_name, "with attribute",
                                           script_attr_name, script_value, ':', e)
                    else:
                        svLogger.log_event('Successfully executed a script for the website', script_website,
                                           "while at url", self.driver.current_url)
                        script_executed = True

                self.driver.switch_to.default_content()

        return script_executed

    def choose_random_locale(self):
        return self.agent_settings.sva_locales[random.randint(0, len(self.agent_settings.sva_locales) - 1)]

    def execute_autorandom_logic(self):
        n_auto_random_clicks = 0
        if self.agent_settings.autorandom_clicks_enabled:
            while n_auto_random_clicks < self.agent_settings.total_autorandom_clicks:
                if self.agent_settings.autorandom_scroll_enabled:
                    self.perform_auto_random_scroll()
                svLogger.log_event("Performing random click #" + str(n_auto_random_clicks + 1) +
                                   " out of total " + str(self.agent_settings.total_autorandom_clicks) +
                                   " clicks in url: " + self.driver.current_url)
                self.perform_auto_random_click()
                n_auto_random_clicks += 1
        elif self.agent_settings.autorandom_scroll_enabled:
            self.perform_auto_random_scroll()

    def perform_auto_random_scroll(self):
        max_scroll_height = self.driver.execute_script("return document.documentElement.scrollHeight;")
        scroll_target = (self.agent_settings.auto_scroll_percent / 100.0) * max_scroll_height
        scroll_position = 0
        scroll_over_time = random.uniform(self.agent_settings.over_scroll_time_min,
                                          self.agent_settings.over_scroll_time_max)
        scroll_speed = scroll_target / scroll_over_time * 0.1

        self.wait_time(
            random.uniform(self.agent_settings.after_scroll_time_min, self.agent_settings.after_scroll_time_max))

        svLogger.log_event("Starting to randomly scroll the page " + self.driver.current_url + " to position " +
                           str(scroll_target) + "/" + str(max_scroll_height) + "px over time: " + str(
            scroll_over_time) + "s")

        while scroll_target - scroll_position > 1.0:
            self.driver.execute_script("window.scrollTo(0, {});".format(scroll_position))
            scroll_position += scroll_speed
            self.wait_time(0.1)

    def perform_auto_random_click(self):
        self.set_wait_interval(self.agent_settings.sva_timeout_interval)

        current_domain = self.extract_domain(self.website)

        xpath_query: str
        if self.agent_settings.click_link_type == VisitWorker.AUTO_RANDOM_ALLOWED_LINKS_TYPES[
            VisitWorker.INTERNAL_LINKS]:
            xpath_query = "//a[contains(normalize-space(@href), '" + current_domain + "')]"
        elif self.agent_settings.click_link_type == VisitWorker.AUTO_RANDOM_ALLOWED_LINKS_TYPES[
            VisitWorker.EXTERNAL_LINKS]:
            xpath_query = "//a[not(contains(normalize-space(@href), '" + current_domain + "'))]"
        else:
            xpath_query = "//a"

        found_elements = self.driver.find_elements_by_xpath(xpath_query)

        svLogger.log_event("Attempting to click on a random link, " + self.agent_settings.click_link_type +
                           " in url: " + self.driver.current_url)

        complete = False
        search_attempts = 0
        max_search_attempts = max(int(len(found_elements) / 2), 2)
        while not complete and search_attempts < max_search_attempts:
            try:
                click_element = found_elements[random.randint(0, len(found_elements) - 1)]
                found_elements.remove(click_element)
                seleniumHelpers.click_element(self.driver, click_element)
            except (ElementClickInterceptedException, ElementNotInteractableException,
                    StaleElementReferenceException) as e:
                search_attempts += 1
                svLogger.log_error("Error clicking on a random link (" + self.agent_settings.click_link_type +
                                   "), retry attempt " + str(search_attempts) + "/" + str(max_search_attempts), e)
            except Exception as e:
                svLogger.log_error("Auto-random click failed (" + self.agent_settings.click_link_type +
                                   "), stopping clicks. Error:", e)
                complete = True
            else:
                svLogger.log_event("Random click success (" + self.agent_settings.click_link_type +
                                   ") in url: " + self.driver.current_url)
                complete = True

        self.driver.switch_to.default_content()
        self.wait_time(random.uniform(self.agent_settings.sva_min_page_time, self.agent_settings.sva_max_page_time))

    def extract_domain(self, url):
        ret_val = re.findall(r'^(?:https?://)?(?:[^@/\n]+@)?(?:www\.)?([^:/?\n]+)', url)[0]
        return ret_val

    def set_wait_interval(self, interval):
        self.driver.implicitly_wait(interval)
        self.driver.set_page_load_timeout(interval)

    def get_thread(self):
        return self.thread

    # rudely interrupts the thread, try-catch is for the case it has been instructed to kill itself, before it could
    # create the driver object
    def kill(self):
        self.alive = False

    def purge(self):
        self.alive = False
        try:
            self.set_wait_interval(0)
            self.driver.quit()
        except:
            pass
        try:
            if self.proxy_plugin_path:
                os.remove(self.proxy_plugin_path)
        except:
            pass

    def join(self):
        try:
            if self.proxy_plugin_path:
                os.remove(self.proxy_plugin_path)
        except:
            pass
        self.scheduler().clear_worker(self)

    def preload_cookies_file(self, target_url):
        """Load cookies whose domain matches the target URL, without mutating source data."""
        cookie_file_path = self.agent_settings.cookies_file
        if not self.agent_settings.sva_cookies_enabled:
            return
        if not os.path.exists(cookie_file_path):
            svLogger.log_event("The", cookie_file_path, "file does not exist. Not using cookies for visit")
            return

        try:
            with open(cookie_file_path, "r", encoding="utf-8") as cookie_file:
                cookies = json.load(cookie_file)
        except (OSError, ValueError) as exc:
            svLogger.log_error("Could not read cookie file", cookie_file_path, exc)
            return

        parsed_url = urlparse(target_url)
        target_hostname = (parsed_url.hostname or "").lower()
        if not parsed_url.scheme or not target_hostname:
            svLogger.log_error("Cannot apply cookies to invalid target URL", target_url)
            return

        target_domain = target_hostname.removeprefix("www.")
        cookie_found = False
        if not isinstance(cookies, list):
            svLogger.log_error("Cookie file must contain a JSON array", cookie_file_path)
            return

        for source_cookie in cookies:
            if not isinstance(source_cookie, dict):
                continue
            cookie = dict(source_cookie)
            cookie_domain = str(cookie.get("domain", "")).lower().lstrip(".")
            cookie_domain = cookie_domain.removeprefix("www.")
            if not cookie_domain or cookie_domain != target_domain:
                continue

            if not cookie_found:
                svLogger.log_event("Found cookie for the website", target_domain, "applying...")
                self.driver.get(f"{parsed_url.scheme}://{parsed_url.hostname}/")
                cookie_found = True

            if self.browser_type == globalConstants.BR_PJS:
                cookie["domain"] = "." + cookie_domain
            if self.browser_type in (globalConstants.BR_CHR, globalConstants.BR_FX):
                cookie.pop("sameSite", None)

            try:
                self.driver.add_cookie(cookie)
            except Exception as exc:
                svLogger.log_error("Failed to apply cookie for", target_domain, exc)

