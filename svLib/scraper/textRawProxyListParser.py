import urllib.request
import re

from svLib.scraper.siteParser import SiteParser
from svLib import globalConstants


class TextRawProxyListParser(SiteParser):
    def __init__(self, s_name, s_url):
        self.s_url = s_url
        super().__init__(s_name, False)

    def scrapProxies(self, driver, do_http, do_https, do_socks, do_transp, do_anon, do_elite, country_list):
        if len(country_list) < 1:
            raise Exception("Select at least one country.")

        proxy_list = []
        do_all_countries = country_list == globalConstants.ALL_COUNTRIES

        self.setAlive(True)

        req = urllib.request.Request(self.s_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0')
        response = urllib.request.urlopen(req)
        raw_text = response.read()
        raw_text = raw_text.decode("utf-8")

        for line in raw_text.split('\n'):
            proxy_addr_match = re.match(r'\d+.\d+.\d+.\d+:\d+', line)

            if proxy_addr_match:
                proxy_addr_line = proxy_addr_match.string

                proxy_addr = re.findall(r'\d+.\d+.\d+.\d+:\d+', proxy_addr_line)[0]

                proxy_flags = re.findall(r'[a-zA-Z]+[-[a-zA-Z]+]*', proxy_addr_line)
                if len(proxy_flags) > 0:
                    flag_list = proxy_flags[0].replace("!", "").split("-")

                    proxy_country = flag_list[0]
                    proxy_anonimity = flag_list[1]
                    is_https = len(flag_list) > 2
                    google_accepted = proxy_addr_line[-2] == "+"

                    if not (do_all_countries or proxy_country in country_list):
                        continue

                    anonimity_satisfied = proxy_anonimity == 'N' and do_transp
                    anonimity_satisfied = anonimity_satisfied or (proxy_anonimity == 'A' and do_anon)
                    anonimity_satisfied = anonimity_satisfied or (proxy_anonimity == 'H' and do_elite)

                    if anonimity_satisfied:
                        if is_https and do_https:
                            proxy_list.append(proxy_addr)
                        elif not is_https and do_http:
                            proxy_list.append(proxy_addr)

        return proxy_list
