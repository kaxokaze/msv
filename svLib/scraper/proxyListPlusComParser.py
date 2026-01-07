import os

from selenium.common.exceptions import TimeoutException

from svLib.log import svLogger
from svLib.scraper.siteParser import SiteParser
from svLib.userData import svSettings
from svLib.utils import stdHelper


class ProxyListPlusComParser(SiteParser):
    def __init__(self):
        self.TYPE_ELITE = "elite"
        self.TYPE_ANONYMOUS = "anonymous"
        self.TYPE_SOCKS4 = "Socks4"
        self.TYPE_SOCKS5 = "Socks5"

        super().__init__("proxylistplus.com", True)

        self.driver = None

        self.do_transparent = False
        self.do_anon = False
        self.do_elite = False
        self.do_socks = False

    def scrapProxies(self, driver, do_http, do_https, do_socks, do_transparent, do_anon, do_elite, country_list):
        self.driver = driver
        self.setAlive(True)

        proxy_list = []

        self.do_transparent = do_transparent
        self.do_anon = do_anon
        self.do_elite = do_elite
        self.do_socks = do_socks

        # get to the page with list of proxies
        try:
            if do_http or do_https:
                if self.do_transparent:
                    self.parsePage('http://list.proxylistplus.com/Fresh-HTTP-Proxy-List-', proxy_list)
                if self.do_anon or self.do_elite:
                    self.parsePage('http://list.proxylistplus.com/SSL-List-', proxy_list)
            if do_socks:
                self.parsePage('http://list.proxylistplus.com/Socks-List-', proxy_list)
        except TimeoutException as e:
            svLogger.log_error('Proxy gathering timed out at some point', e)
        except:
            pass

        return proxy_list

    def parsePage(self, web__base_url, proxy_list):
        if not self.isAlive():
            return

        # starting from page1
        curr_page_num = 1
        web_url = web__base_url + str(curr_page_num)

        self.driver.implicitly_wait(SiteParser.SCRAP_LOADING_TIMEOUT)
        self.driver.get(web_url)

        svLogger.log_event('Got the proxy dir default page', web_url)
        self.driver.save_screenshot(os.path.join(svSettings.program_data_folder, 'scraps', 'proxylistplus1.png'))

        next_page_link = 'heh, kid, i wish there was a do-while loop, nothing personnel'
        while (next_page_link is not None) and curr_page_num < 20:
            if not self.isAlive():
                return

            # table with the list of proxies, find it
            table = self.driver.find_element_by_xpath("//table[2]")
            self.driver.implicitly_wait(0)
            tab_rows = table.find_elements_by_xpath(".//tbody/tr")

            svLogger.log_event('Scraping the proxy table from page index', curr_page_num, 'at proxylistplus.com')
            self.driver.save_screenshot(os.path.join(svSettings.program_data_folder, 'scraps', 'proxylistplus2.png'))

            # rows with the proxies
            for row in tab_rows:
                try:
                    ip_col = row.find_element_by_xpath(".//td[2]")
                    port_col = row.find_element_by_xpath(".//td[3]")
                    type_col = row.find_element_by_xpath(".//td[4]")
                    proxy_type = type_col.text

                    is_socks = proxy_type == self.TYPE_SOCKS4 or proxy_type == self.TYPE_SOCKS5
                    is_anon = proxy_type == self.TYPE_ANONYMOUS
                    is_elite = proxy_type == self.TYPE_ELITE

                    proxy_addr = str(ip_col.text) + ":" + str(port_col.text) + (' ' + proxy_type.lower() if is_socks else '')

                    scrap_this = self.do_anon and is_anon or \
                        self.do_elite and is_elite or \
                        is_socks and self.do_socks

                    if scrap_this and stdHelper.isProxyString(proxy_addr):
                        stdHelper.addToArray(proxy_list, proxy_addr)
                except:
                    pass

            # find the navigation links, determine current page
            try:
                nav_tab = self.driver.find_element_by_xpath("//table[3]")
                nav_td = nav_tab.find_element_by_xpath(".//tr[1]")
            except:
                next_page_link = None
            else:
                # find the link to the next page (if it exists)
                curr_page_num += 1
                try:  # Why couldn't those retards just return None if no element is found, instead of throwing an exception?
                    next_page_link = nav_td.find_element_by_xpath(
                        "//a[contains(text(), '[" + str(curr_page_num) + "]')]")
                except:
                    next_page_link = None
                else:
                    web_url = web__base_url + str(curr_page_num)
                    self.driver.get(web_url)
                    self.driver.implicitly_wait(SiteParser.SCRAP_LOADING_TIMEOUT)
