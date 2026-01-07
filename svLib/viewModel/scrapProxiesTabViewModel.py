import tkinter

from svLib import globalConstants
from svLib.gui.scrapProxiesTab import ScrapProxiesTab
from svLib.viewModel.helpers import saveAsFilenameDial


class ScrapProxiesTabViewModel:
    def __init__(self, scrap_proxies_tab: ScrapProxiesTab, proxy_directory_sites: list,
                 start_prox_gather_clk_callback, stop_prox_gather_clk_callback, default_impor_prx_file):
        self.scrap_proxies_tab = scrap_proxies_tab

        # Proxy scraper tab
        self.http_pr_search_on = tkinter.IntVar()
        self.http_pr_search_on.set(1)
        self.scrap_proxies_tab.bind_http_chk_btn(self.http_pr_search_on, self.on_http_pr_search_check)

        self.https_pr_search_on = tkinter.IntVar()
        self.https_pr_search_on.set(1)
        self.scrap_proxies_tab.bind_https_chk_btn(self.https_pr_search_on, self.on_https_pr_search_check)

        self.transparent_pr_search_on = tkinter.IntVar()
        self.transparent_pr_search_on.set(0)
        self.scrap_proxies_tab.bind_transp_chk_btn(self.transparent_pr_search_on, None)

        self.anon_pr_search_on = tkinter.IntVar()
        self.anon_pr_search_on.set(1)
        self.scrap_proxies_tab.bind_anon_chk_btn(self.anon_pr_search_on, None)

        self.elite_pr_search_on = tkinter.IntVar()
        self.elite_pr_search_on.set(1)
        self.scrap_proxies_tab.bind_elite_chk_btn(self.elite_pr_search_on, None)

        self.socks_pr_search_on = tkinter.IntVar()
        self.socks_pr_search_on.set(1)
        self.scrap_proxies_tab.bind_socks_chk_btn(self.socks_pr_search_on, self.on_socks_pr_search_check)

        self.scrap_proxies_tab.bind_start_prox_gather_btn(start_prox_gather_clk_callback)
        self.scrap_proxies_tab.bind_stop_prox_gather_btn(stop_prox_gather_clk_callback)

        self.proxy_directory_sites = []
        self.current_proxy_directory_site = tkinter.StringVar()
        self.setProxyDirectorySites(proxy_directory_sites)

        self.current_proxy_imp_file = tkinter.StringVar()
        self.current_proxy_imp_file.set(default_impor_prx_file)

        self.scrap_proxies_tab.bindImportProxToEntry(self.current_proxy_imp_file)
        self.scrap_proxies_tab.bindChooImportProxFileBtn(self.onChooseImpProxyFileClick)

        self.countries_to_scrap = {}
        for country_code, country_name in globalConstants.COUNTRY_CODES.items():
            country_var = tkinter.IntVar()
            country_var.set(1)
            self.scrap_proxies_tab.create_and_bind_country_chk_btn(country_code, country_name, country_var,
                                                                   self.on_country_select_check)
            self.countries_to_scrap[country_code] = country_var

        self.scrap_proxies_tab.bindDeselectAllCountriesBtn(self.onDeselectAllProxies)
        self.scrap_proxies_tab.bindSelectAllCountriesBtn(self.onSelectAllProxies)

        # proxy scraper - load into the program checkbox
        self.load_rightaway = tkinter.IntVar()
        self.load_rightaway.set(1)
        self.scrap_proxies_tab.bind_load_rightaway(self.load_rightaway)

    ###
    # API
    ###

    def setProxyDirectorySites(self, proxy_directory_sites):
        self.proxy_directory_sites = proxy_directory_sites
        self.current_proxy_directory_site.set(self.proxy_directory_sites[0])
        self.scrap_proxies_tab.bind_proxy_list_cmbbx(self.proxy_directory_sites,
                                                     self.current_proxy_directory_site)

    def is_load_rightaway_on(self):
        return self.load_rightaway.get() == 1

    def get_proxy_import_file(self):
        return self.current_proxy_imp_file.get()

    def is_http_gather_on(self):
        return self.http_pr_search_on.get() == 1

    def is_https_gather_on(self):
        return self.https_pr_search_on.get() == 1

    def is_socks_gather_on(self):
        return self.socks_pr_search_on.get() == 1

    def is_transp_gather_on(self):
        return self.transparent_pr_search_on.get() == 1

    def is_anon_gather_on(self):
        return self.anon_pr_search_on.get() == 1

    def is_elite_gather_on(self):
        return self.elite_pr_search_on.get() == 1

    def state_enabled_stop_proxy_gather_btn(self):
        self.scrap_proxies_tab.state_enabled_stop_proxy_gather_btn()

    def state_gathering_stop_proxy_gather_btn(self):
        self.scrap_proxies_tab.state_gathering_stop_proxy_gather_btn()

    def state_stopping_stop_proxy_gather_btn(self):
        self.scrap_proxies_tab.state_stopping_stop_proxy_gather_btn()

    def state_disabled_import_proxy_file_btn(self):
        self.scrap_proxies_tab.state_disabled_import_proxy_file_btn()

    def state_enabled_import_proxy_file_btn(self):
        self.scrap_proxies_tab.state_enabled_import_proxy_file_btn()

    def is_proxy_start_gather_enabled(self):
        return self.scrap_proxies_tab.is_proxy_start_gather_enabled()

    def is_proxy_start_gather_gathering(self):
        return self.scrap_proxies_tab.is_proxy_start_gather_gathering()

    def is_proxy_start_gather_stopping(self):
        return self.scrap_proxies_tab.is_proxy_start_gather_stopping()

    def get_current_proxy_provider(self):
        return self.current_proxy_directory_site.get()

    def getProxyCountries(self):
        selected_countries = [k for k, v in self.countries_to_scrap.items() if v.get() == 1]

        if len(selected_countries) == len(self.countries_to_scrap):
            return globalConstants.ALL_COUNTRIES
        return selected_countries

    ###
    # Callbacks
    ###

    def onChooseImpProxyFileClick(self):
        filename = saveAsFilenameDial('Save imported proxies to...')
        if filename:
            self.current_proxy_imp_file.set(filename)

    def on_http_pr_search_check(self):
        pass

    def on_https_pr_search_check(self):
        pass

    def on_socks_pr_search_check(self):
        pass

    def on_country_select_check(self):
        pass

    def onDeselectAllProxies(self):
        for country_var in self.countries_to_scrap.values():
            country_var.set(0)

    def onSelectAllProxies(self):
        for country_var in self.countries_to_scrap.values():
            country_var.set(1)
