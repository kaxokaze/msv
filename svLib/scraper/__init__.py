from svLib.log import svLogger
from svLib.scraper.freeProxyListComParser import FreeProxyListComParser
from svLib.scraper.textRawProxyListParser import TextRawProxyListParser
from svLib.scraper.proxyListPlusComParser import ProxyListPlusComParser
from svLib.scraper.proxyNovaComParser import ProxyNovaComParser
from svLib.scraper.proxyScrapeComParser import ProxyScrapeComParser
from svLib.scraper.pubProxyComParser import PubProxyComParser
from svLib.scraper.scraperModel import ScraperModel
from svLib.scraper.proxyScraper import ProxyScraper

svps_scraper: ProxyScraper = None
scraper_model: ScraperModel = ScraperModel()

svps_site_scrapers_map: dict = {
    'proxyscrape.com': (1, ProxyScrapeComParser()),
    'spys.me': (2, TextRawProxyListParser("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
                                          "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt")),
    'proxynova.com': (3, ProxyNovaComParser()),
    'free-proxy-list.net': (4, FreeProxyListComParser()),
    'proxylistplus.com': (5, ProxyListPlusComParser()),
    'pubproxy.com': (6, PubProxyComParser()),
    'github.com/clarketm/proxy-list': (7, TextRawProxyListParser("https://github.com/clarketm/proxy-list/",
                                                                 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'))
}


######################
# API of the module
######################

def get_list_of_proxy_dirs():
    directory_sites = list(svps_site_scrapers_map.keys())
    directory_sites.sort(key=lambda x: svps_site_scrapers_map[x][0])
    return directory_sites


def start_gathering(directory_site_name, do_http, do_https, do_socks, import_target, on_proxies_gather_complete,
                    on_proxies_gather_fail,
                    do_transparent, do_anon, do_elite, country_list):
    scraper_model.svps_gathered_callback = on_proxies_gather_complete
    scraper_model.svps_failed_callback = on_proxies_gather_fail

    # if something's running - kill it first
    global svps_scraper
    if svps_scraper is not None:
        svps_scraper.kill()

    # only then we start a new scraping session
    svps_scraper = ProxyScraper(scraper_model, choose_site_parser(directory_site_name), do_http, do_https, do_socks,
                                import_target, do_transparent, do_anon, do_elite, country_list)
    svps_scraper.start()


def stop_gathering():
    if svps_scraper is not None:
        svLogger.log_event('Stopping proxy gathering')
        svps_scraper.kill()


def choose_site_parser(directory_site_url):
    directory_sites = get_list_of_proxy_dirs()
    for site_name in directory_sites:
        if site_name in directory_site_url:
            return svps_site_scrapers_map[site_name][1]
