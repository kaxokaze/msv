import threading

from svLib.log import svLogger
from svLib.scraper import ScraperModel
from svLib.scraper.siteParser import SiteParser
from svLib.system import childProcessesManager
from svLib.utils import seleniumHelpers


######################
# Class that spawns a separate thread, that does the whole scrapping routine
# to get the list of proxies from some web-site
######################
class ProxyScraper:
    def __init__(self, scraper_model: ScraperModel, site_parser: SiteParser, do_http, do_https, do_socks, import_target,
                 do_transparent, do_anon, do_elite, country_list):
        self.scraper_model = scraper_model
        self.site_parser = site_parser
        self.driver = None
        self.alive = True

        self.thread = threading.Thread(target=self.scrapProxies, args=(
            do_http, do_https, do_socks, import_target, do_transparent, do_anon, do_elite, country_list))

    def start(self):
        if not self.alive:
            return

        self.thread.start()

    def scrapProxies(self, do_http, do_https, do_socks, import_target, do_transp, do_anon, do_elite, country_list):
        # we can always be stopped prematurely by user actions (click on the gui)
        if not self.alive:
            return

        svLogger.log_event('Starting proxy gathering from', self.site_parser.getSiteUrl(), do_http, do_https,
                           do_socks, import_target)

        if self.site_parser.usesSelenium():
            self.driver = self.createScrapingDriver()
            self.driver.set_window_size(1920, 1100)
            self.driver.implicitly_wait(self.scraper_model.svps_proxy_gather_timeout)
            self.driver.set_page_load_timeout(self.scraper_model.svps_proxy_gather_timeout)
            childProcessesManager.ignorePid(self.driver.service.process.pid)

        if not self.alive:
            self.purge()
            return

        try:
            proxies = self.site_parser.scrapProxies(self.driver, do_http, do_https, do_socks, do_transp, do_anon,
                                                    do_elite, country_list)

            svLogger.log_event('Gathered', len(proxies), 'proxies from', self.site_parser.getSiteUrl())
        except Exception as e:
            svLogger.log_error('Failed to scrap proxies from', self.site_parser.getSiteUrl(), e)
            if self.scraper_model.svps_failed_callback is not None:
                self.scraper_model.svps_failed_callback()
        else:
            try:
                if len(proxies) > 0:
                    with open(import_target, 'w+') as save_file:
                        for proxy in proxies:
                            save_file.write(proxy + '\n')
            except Exception as e:
                svLogger.log_error('Failed to save the proxy to the file %s.' % import_target, e)

            # After all is said and done, send back the msg about success to the caller
            if self.scraper_model.svps_gathered_callback is not None:
                self.scraper_model.svps_gathered_callback()

        try:
            if self.driver is not None:
                childProcessesManager.unIgnorePid(self.driver.service.process.pid)
                self.driver.quit()
        except:
            pass

    def createScrapingDriver(self):
        try:
            return seleniumHelpers.createHeadlessChromeDriver()
        except Exception as e:
            try:
                return seleniumHelpers.createPhantomJsDriver()
            except Exception as e:
                try:
                    return seleniumHelpers.createHeadlessFirefoxDriver()
                except Exception as e:
                    return None

    def kill(self):
        if self.alive:
            self.alive = False
            if self.site_parser is not None:
                self.site_parser.kill()

    # None shall survive
    def purge(self):
        try:
            if self.driver is not None:
                self.driver.close()
                self.driver.quit()
        except Exception as e:
            print(e)
