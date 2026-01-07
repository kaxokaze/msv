import random
import re
import os
import time

from selenium.common.exceptions import TimeoutException

from svLib.log import svLogger
from svLib.scraper.siteParser import SiteParser
from svLib.userData import svSettings
from svLib.utils import stdHelper
from svLib import globalConstants


class ProxyNovaComParser(SiteParser):
    def __init__(self):
        self.BASE_NOVA_URL = "http://www.proxynova.com/proxy-server-list/country-"

        self.NOVA_TYPE_ELITE = "Elite"
        self.NOVA_TYPE_ANONYMOUS = "Anonymous"
        self.NOVA_TYPE_TRANSPARENT = "Transparent"

        super().__init__("proxynova.com", True)

        self.driver = None
        self.do_transp = False
        self.do_anon = False
        self.do_elite = False

        self.do_all_countries = False
        self.country_list = None

    def scrapProxies(self, driver, do_http, do_https, do_socks, do_transp, do_anon, do_elite, country_list):
        if len(country_list) < 1:
            raise Exception("Select at least one country.")

        proxy_list = []

        self.driver = driver
        self.do_transp = do_transp
        self.do_anon = do_anon
        self.do_elite = do_elite

        self.do_all_countries = country_list == globalConstants.ALL_COUNTRIES
        self.country_list = country_list

        self.setAlive(True)

        try:
            # get to the page with list of proxies
            pages = self.get_nova_pages_list('https://www.proxynova.com/proxy-server-list/')

            for page in pages:
                if not self.isAlive():
                    break

                try:
                    self.parsePage(page, proxy_list)
                except Exception as e:
                    svLogger.log_error('Failed parsing proxynova page', page, e)

                time.sleep(random.uniform(0.15, 1.39))

        except TimeoutException as e:
            svLogger.log_error('Proxy gathering timed out at some point')
        except:
            pass

        return proxy_list

    def get_nova_pages_list(self, origin_page):
        page_list = []

        if not self.isAlive():
            return []

        self.driver.implicitly_wait(SiteParser.SCRAP_LOADING_TIMEOUT)

        self.driver.get(origin_page)
        svLogger.log_event('Got the novaproxy default page', origin_page)
        self.driver.save_screenshot(os.path.join(svSettings.program_data_folder, 'scraps', 'novaproxy1.png'))

        country_selection = self.driver.find_element_by_xpath("//select[@name='proxy_country']")
        country_options = country_selection.find_elements_by_tag_name("option")

        for country_option in country_options:
            numbers = re.findall(r'(\d+)', country_option.text)
            if len(numbers) > 0:
                country_proxy_amount = int(numbers[0])
                if country_proxy_amount > 0:
                    country_tag = country_option.get_attribute("value").upper()
                    if self.do_all_countries or country_tag in self.country_list:
                        page_list.append(self.BASE_NOVA_URL + country_tag)

        return page_list

    def parsePage(self, web_url, proxy_list):
        if not self.isAlive():
            return

        self.driver.implicitly_wait(SiteParser.SCRAP_LOADING_TIMEOUT)

        self.driver.get(web_url)
        svLogger.log_event('navigated to the proxy page', web_url)
        self.driver.save_screenshot(os.path.join(svSettings.program_data_folder, 'scraps', 'novaproxy2.png'))

        # table with the list of proxies, find it
        table = self.driver.find_element_by_xpath("//table[@id='tbl_proxy_list']")
        tab_rows = table.find_elements_by_xpath(".//tbody/tr")
        # rows with the proxies
        svLogger.log_event('Scraping the proxy table from page ', web_url, 'at novaproxy.com')

        for row in tab_rows:
            try:
                self.driver.implicitly_wait(0)

                ip_col = row.find_element_by_xpath(".//td[1]")
                port_col = row.find_element_by_xpath(".//td[2]")
                type_col = row.find_element_by_xpath(".//td[7]")

                proxy_addr = str(ip_col.text) + ":" + str(port_col.text)

                proxy_type = type_col.text

                scrap_this = self.do_transp and proxy_type == self.NOVA_TYPE_TRANSPARENT or \
                             self.do_anon and proxy_type == self.NOVA_TYPE_ANONYMOUS or \
                             self.do_elite and proxy_type == self.NOVA_TYPE_ELITE

                if scrap_this and stdHelper.isProxyString(proxy_addr):
                    stdHelper.addToArray(proxy_list, proxy_addr)
            except Exception as e:
                pass
