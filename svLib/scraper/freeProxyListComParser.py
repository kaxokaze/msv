import time
import os

from selenium.common.exceptions import TimeoutException

from svLib.log import svLogger
from svLib.scraper.siteParser import SiteParser
from svLib.userData import svSettings
from svLib.utils import stdHelper
from svLib import globalConstants


class FreeProxyListComParser(SiteParser):
    def __init__(self):
        self.TYPE_ELITE = "elite proxy"
        self.TYPE_ANONYMOUS = "anonymous"
        self.TYPE_TRANSPARENT = "transparent"

        self.URL_HTTP = 'https://free-proxy-list.net/'
        self.URL_HTTPS = 'https://www.sslproxies.org/'
        self.URL_SOCKS = 'https://www.socks-proxy.net/'

        super().__init__("free-proxy-list.net", True)

        self.driver = None

        self.do_transparent = False
        self.do_anon = False
        self.do_elite = False
        self.do_socks = False

        self.do_all_countries = False
        self.country_list = None

    def scrapProxies(self, driver, do_http, do_https, do_socks, do_transp, do_anon, do_elite, country_list):
        if len(country_list) < 1:
            raise Exception("Select at least one country.")

        proxy_list = []

        self.driver = driver

        self.do_transparent = do_transp
        self.do_anon = do_anon
        self.do_elite = do_elite
        self.do_socks = do_socks

        self.do_all_countries = country_list == globalConstants.ALL_COUNTRIES
        self.country_list = country_list

        self.setAlive(True)

        # get to the page with list of proxies
        try:
            if do_http:
                self.parsePage(self.URL_HTTP, proxy_list)

            if do_https:
                self.parsePage(self.URL_HTTPS, proxy_list)

            if do_socks:
                self.parsePage(self.URL_SOCKS, proxy_list)

        except TimeoutException as e:
            svLogger.log_error('Proxy gathering timed out at some point')
        except Exception as e:
            pass

        return proxy_list

    def parsePage(self, web_url, proxy_list):
        if not self.isAlive():
            return

        self.driver.implicitly_wait(SiteParser.SCRAP_LOADING_TIMEOUT)
        self.driver.get(web_url)

        svLogger.log_event('Got the proxy dir default page', web_url)
        self.driver.save_screenshot(os.path.join(svSettings.program_data_folder, 'scraps', 'free-proxy-list1.png'))

        next_page_link = 'heh, kid, i wish there was a do-while loop, nothing personnel'
        curr_page_num = 1
        next_is_active = True
        while next_is_active and (next_page_link is not None) and curr_page_num < 20:
            if not self.isAlive():
                return

            # table with the list of proxies, find it
            table = self.driver.find_element_by_xpath("//section[@id='list']//table")
            self.driver.implicitly_wait(0)
            tab_rows = table.find_elements_by_xpath(".//tbody/tr")

            svLogger.log_event('Scraping the proxy table from page index', curr_page_num, 'at free-proxy-list.net')
            self.driver.save_screenshot(os.path.join(svSettings.program_data_folder, 'scraps', 'free-proxy-list2.png'))

            # rows with the proxies
            for row in tab_rows:
                try:
                    ip_col = row.find_element_by_xpath(".//td[1]")
                    port_col = row.find_element_by_xpath(".//td[2]")
                    country_code_col = row.find_element_by_xpath(".//td[3]")
                    proxy_type_col = row.find_element_by_xpath(".//td[5]")

                    country_code = country_code_col.text
                    proxy_type = proxy_type_col.text

                    is_transparent = proxy_type == self.TYPE_TRANSPARENT
                    is_anonymous = proxy_type == self.TYPE_ANONYMOUS
                    is_elite = proxy_type == self.TYPE_ELITE
                    is_socks = web_url == self.URL_SOCKS

                    proxy_addr = str(ip_col.text) + ":" + str(port_col.text) + (' ' + proxy_type.lower() if is_socks else '')

                    scrap_this = self.do_transparent and is_transparent or \
                        self.do_anon and is_anonymous or \
                        self.do_elite and is_elite or \
                        self.do_socks and is_socks

                    scrap_this = scrap_this and (self.do_all_countries or country_code in self.country_list)

                    if scrap_this and stdHelper.isProxyString(proxy_addr):
                        stdHelper.addToArray(proxy_list, proxy_addr)
                except:
                    pass

            # find the navigation links, determine current page
            try:
                nav_div = self.driver.find_element_by_xpath("//div[@id='proxylisttable_paginate']")
                next_li = nav_div.find_element_by_xpath(".//li[@id='proxylisttable_next']")
                next_page_link = next_li.find_element_by_xpath(".//a")
                class_attr = next_li.get_attribute("class")
                next_is_active = "disabled" not in class_attr
            except:
                next_page_link = None
            else:
                try:
                    if next_is_active:
                        next_page_link.click()
                        time.sleep(0.1)
                        self.driver.implicitly_wait(SiteParser.SCRAP_LOADING_TIMEOUT)
                except Exception as e:
                    pass
                curr_page_num += 1
