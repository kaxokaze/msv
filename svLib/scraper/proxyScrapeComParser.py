import urllib.request
from urllib.error import HTTPError
import time

from svLib.log import svLogger
from svLib.scraper.siteParser import SiteParser
from svLib import globalConstants


class ProxyScrapeComParser(SiteParser):
    def __init__(self):
        super().__init__("https://proxyscrape.com/free-proxy-list", False)

    def scrapProxies(self, driver, do_http, do_https, do_socks, do_transp, do_anon, do_elite, country_list):
        if len(country_list) < 1:
            raise Exception("Select at least one country.")

        proxy_list = []

        self.setAlive(True)

        if do_http or do_https:
            ssl = "all"
            if do_http and not do_https:
                ssl = "no"
            elif do_https and not do_http:
                ssl = "yes"

            if do_transp:
                self.scrapHttpProxiesPerCountry(
                    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country={0}&ssl={1}&anonymity={2}&simplified=true',
                    proxy_list, country_list, ssl, "transparent")
            if do_anon:
                self.scrapHttpProxiesPerCountry(
                    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country={0}&ssl={1}&anonymity={2}&simplified=true',
                    proxy_list, country_list, ssl, "anonymous")
            if do_elite:
                self.scrapHttpProxiesPerCountry(
                    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country={0}&ssl={1}&anonymity={2}&simplified=true',
                    proxy_list, country_list, ssl, "elite")

        if do_socks:
            self.scrapSocksProxiesPerCountry(
                'https://api.proxyscrape.com/v2/?request=getproxies&protocol={0}&timeout=10000&country={1}',
                proxy_list, country_list, "socks5"
            )
            self.scrapSocksProxiesPerCountry(
                'https://api.proxyscrape.com/v2/?request=getproxies&protocol={0}&timeout=10000&country={1}',
                proxy_list, country_list, "socks4"
            )

        return proxy_list

    def scrapHttpProxiesPerCountry(self, url_format, proxy_list, country_list, ssl, anonimity):
        do_all_countries = country_list == globalConstants.ALL_COUNTRIES

        if do_all_countries:
            proxyscrape_url = url_format.format("all", ssl, anonimity)
            self.extractProxyFromApi(proxyscrape_url, proxy_list, None)
        else:
            i = 0
            for country in country_list:
                if not self.isAlive():
                    break
                i += 1
                proxyscrape_url = url_format.format(country, ssl, anonimity)
                if i % 19 == 0:
                    time.sleep(5)
                self.extractProxyFromApi(proxyscrape_url, proxy_list, None)

    def scrapSocksProxiesPerCountry(self, url_format, proxy_list, country_list, socks_version):
        do_all_countries = country_list == globalConstants.ALL_COUNTRIES

        if do_all_countries:
            proxyscrape_url = url_format.format(socks_version, "all")
            self.extractProxyFromApi(proxyscrape_url, proxy_list, socks_version)
        else:
            for country in country_list:
                proxyscrape_url = url_format.format(socks_version, country)
                self.extractProxyFromApi(proxyscrape_url, proxy_list, socks_version)

    def extractProxyFromApi(self, api_url, proxy_list, socks_type):
        if not self.isAlive():
            return

        svLogger.log_event('Parsing proxies from api:', api_url)

        success = False
        n_tries = 0
        raw_text = ""
        while not success and n_tries < 5 and self.isAlive():
            try:
                n_tries += 1
                response = urllib.request.urlopen(api_url)
                raw_text = response.read()
            except HTTPError:
                time.sleep(5 * n_tries)
            else:
                success = True
        raw_text = raw_text.decode("utf-8")

        for line in raw_text.split('\n'):
            if len(line) > 1:
                if socks_type:
                    proxy_list.append(line[:-1] + " " + socks_type)
                else:
                    proxy_list.append(line[:-1])
