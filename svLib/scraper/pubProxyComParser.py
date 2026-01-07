import random
import urllib.request
from urllib.error import HTTPError
import time

from svLib.log import svLogger
from svLib.scraper.siteParser import SiteParser
from svLib import globalConstants


class PubProxyComParser(SiteParser):
    def __init__(self):
        super().__init__("http://pubproxy.com/", False)

    def scrapProxies(self, driver, do_http, do_https, do_socks, do_transp, do_anon, do_elite, country_list):
        if len(country_list) < 1:
            raise Exception("Select at least one country.")

        proxy_list = []

        self.setAlive(True)

        if do_http or do_https:
            proxy_type = "&type=http"
            https_param = ""
            if do_http and not do_https:
                https_param = "&https=false"
            elif do_https and not do_http:
                https_param = "&https=true"

            base_api_url = "http://pubproxy.com/api/proxy?format=txt&limit=5&speed=60" \
                           + https_param + proxy_type
            if do_transp:
                self.scrap_http_proxies_per_country(
                    base_api_url,
                    proxy_list, country_list)
            if do_anon:
                self.scrap_http_proxies_per_country(
                    base_api_url + "&level=anonymous",
                    proxy_list, country_list)
            if do_elite:
                self.scrap_http_proxies_per_country(
                    base_api_url + "&level=elite",
                    proxy_list, country_list)

        if do_socks:
            self.scrap_socks_proxies_per_country(
                "http://pubproxy.com/api/proxy?format=txt&limit=5&speed=60&type=socks4",
                proxy_list, country_list, "socks5"
            )
            self.scrap_socks_proxies_per_country(
                "http://pubproxy.com/api/proxy?format=txt&limit=5&speed=60&type=socks5",
                proxy_list, country_list, "socks4"
            )

        return proxy_list

    def scrap_http_proxies_per_country(self, api_url, proxy_list, country_list):
        do_all_countries = country_list == globalConstants.ALL_COUNTRIES

        if do_all_countries:
            self.extract_proxies_from_api_repeatedly(api_url, proxy_list, None)
        else:
            country_list = ",".join(country_list).lower()

            api_url = api_url + "&country={0}"
            api_url = api_url.format(country_list)

            self.extract_proxies_from_api_repeatedly(api_url, proxy_list, None)

    def scrap_socks_proxies_per_country(self, api_url, proxy_list, country_list, socks_version):
        do_all_countries = country_list == globalConstants.ALL_COUNTRIES

        if do_all_countries:
            self.extract_proxies_from_api_repeatedly(api_url, proxy_list, socks_version)
        else:
            country_list = ",".join(country_list).lower()

            api_url = api_url + "&country={0}"
            api_url = api_url.format(country_list)

            self.extract_proxies_from_api_repeatedly(api_url, proxy_list, socks_version)

    def extract_proxies_from_api_repeatedly(self, api_url, proxy_list, socks_type):
        for i in range(15):
            if not self.isAlive():
                return False

            time.sleep(random.uniform(1.1, 1.9))

            if not self.extract_proxy_from_api(api_url, proxy_list, socks_type):
                self.setAlive(False)
                return False

            if i % 4 == 0:
                time.sleep(random.uniform(2, 4))

        return True

    def extract_proxy_from_api(self, api_url, proxy_list, socks_type):
        if not self.isAlive():
            return False

        svLogger.log_event('Parsing proxies from api:', api_url)

        success = False
        n_tries = 0
        raw_text = ""
        while not success and n_tries < 5 and self.isAlive():
            try:
                n_tries += 1
                response = urllib.request.urlopen(api_url)
                raw_text = response.read()
            except HTTPError as e:
                time.sleep(5 * n_tries)
                err_response = e.read()
                if err_response.startswith(b'You reached the maximum') or e.code == 503:
                    svLogger.log_error('Max proxy scraping for today reached for pubproxy.com.', err_response)
                    return False
            else:
                success = True

        try:
            raw_text = raw_text.decode("utf-8")

            for line in raw_text.split('\n'):
                if len(line) > 1:
                    if socks_type:
                        proxy_list.append(line[:-1] + " " + socks_type)
                    else:
                        proxy_list.append(line[:-1])
        except Exception as e:
            svLogger.log_error('Error extracting proxies from the response:', e)

        return True
