from svLib.gui.mainWindow import MainWindow
from svLib.viewModel.eventsTabViewModel import EventsTabViewModel
from svLib.viewModel.helpers import saveAsFileDial
from svLib.viewModel.mainTabViewModel import MainTabViewModel
from svLib.viewModel.optionsTabViewModel import OptionsTabViewModel
from svLib.viewModel.scrapProxiesTabViewModel import ScrapProxiesTabViewModel
from svLib.viewModel.userScriptsTabViewModel import UserScriptsTabViewModel


class MainWindowViewModel:
    def __init__(self, main_window, link_types: list, proxy_directory_sites: list,
                 on_save_options, on_options_discard, on_options_reset_default,
                 default_website='', default_views='100', default_threads='10', ref_callback=None, ua_callback=None,
                 proxy_callback=None, snapshot_toggle_callback=None, only_success_toggle_callback=None,
                 start_prox_gather_clk_callback=None,
                 stop_prox_gather_clk_callback=None, default_impor_prx_file='', br_swit_callback=None,
                 on_hide_offscreen_switch=None, on_headless_mode_switch=None,
                 test_prox_callback=None, on_clear_prox=None, default_cookies_file=''):
        self.main_window: MainWindow = main_window

        self.main_tab_vm = MainTabViewModel(self.main_window.main_tab, default_website, default_views, br_swit_callback,
                                            default_threads, on_hide_offscreen_switch, on_headless_mode_switch,
                                            ref_callback, ua_callback, proxy_callback, test_prox_callback,
                                            on_clear_prox)

        self.on_options_discard_callback = on_options_discard
        self.on_save_options_callback = on_save_options

        self.options_tab_vm = OptionsTabViewModel(self.main_window.options_tab, snapshot_toggle_callback,
                                                  only_success_toggle_callback,
                                                  self.on_save_options, self.on_options_discard,
                                                  on_options_reset_default, self.on_options_change, default_cookies_file)

        self.user_scripts_tab_vm = UserScriptsTabViewModel(self.main_window.user_scripts_tab, link_types,
                                                           self.on_save_userscripts, self.on_userscripts_discard,
                                                           on_options_reset_default, self.on_userscripts_change)

        self.events_tab_vm = EventsTabViewModel(self.main_window.events_tab)

        self.scrap_proxies_tab_vm = ScrapProxiesTabViewModel(self.main_window.scrap_proxies_tab,
                                                             proxy_directory_sites,
                                                             start_prox_gather_clk_callback,
                                                             stop_prox_gather_clk_callback,
                                                             default_impor_prx_file)

        self.main_window.bindExportHealthyProxies(self.exportHealthyProxies)
        self.main_window.bindExportNonLaggedProxies(self.exportNonLaggedProxies)
        self.main_window.bindSaveLog(self.saveLogToAFile)

    ################################
    # ''''''''API'''''''' of the model
    ################################

    def setThreadsActive(self, value):
        self.main_tab_vm.setThreadsActive(value)
        self.events_tab_vm.setThreadsActive(value)

    def setTitle(self, title):
        self.main_window.setTitle(title)

    ################################
    # Callbacks and other things for internal usage
    ################################

    def on_options_change(self):
        self.user_scripts_tab_vm.show_new_changes_to_ui()

    def on_userscripts_change(self):
        self.options_tab_vm.show_new_changes_to_ui()

    def on_save_options(self):
        self.on_save_options_callback()
        self.user_scripts_tab_vm.remove_new_changes_from_ui()

    def on_save_userscripts(self):
        self.on_save_options_callback()
        self.options_tab_vm.remove_new_changes_from_ui()

    def on_options_discard(self):
        self.on_options_discard_callback()
        self.user_scripts_tab_vm.remove_new_changes_from_ui()

    def on_userscripts_discard(self):
        self.on_options_discard_callback()
        self.options_tab_vm.remove_new_changes_from_ui()

    def exportHealthyProxies(self):
        c_file = saveAsFileDial("Export healthy proxies to a file")
        if c_file is None:
            return

        with c_file:
            self.main_tab_vm.export_healthy_proxies(c_file)

    def exportNonLaggedProxies(self):
        c_file = saveAsFileDial("Export healthy proxies to a file")
        if c_file is None:
            return

        with c_file:
            self.main_tab_vm.export_non_lagging_proxies(c_file)

    def saveLogToAFile(self):
        c_file = saveAsFileDial("Save the log to a file")
        if c_file is None:
            return

        with c_file:
            self.events_tab_vm.save_log_to_file(c_file)
