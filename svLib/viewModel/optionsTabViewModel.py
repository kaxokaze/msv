import re
import tkinter

from svLib.viewModel.helpers import saveAsFilenameDial, openFilenameDial
from svLib.viewModel.settingsViewModel import SettingsViewModel


class OptionsTabViewModel(SettingsViewModel):
    def __init__(self, options_tab, snapshot_toggle_callback, only_success_toggle_callback,
                 on_save_options, on_options_discard, on_options_reset_default, on_ui_changed, default_cookies_file):
        super().__init__(options_tab, on_save_options, on_options_discard, on_options_reset_default, on_ui_changed)

        self.options_tab = options_tab
        
        # Options menu vars
        self.min_pg_time = tkinter.StringVar()
        self.options_tab.bind_min_pg_time(self.min_pg_time)

        self.max_pg_time = tkinter.StringVar()
        self.options_tab.bind_max_pg_time(self.max_pg_time)

        self.after_script_wait = tkinter.StringVar()
        self.options_tab.bind_after_script_wait_entry(self.after_script_wait)

        self.snapshot_var = tkinter.IntVar()
        self.snapshot_var.set(1)
        self.options_tab.bindSnapCheckBox(self.snapshot_var, self.on_snapshot_check)
        self.snapshot_toggle_callback = snapshot_toggle_callback

        self.only_succ_var = tkinter.IntVar()
        self.only_succ_var.set(1)
        self.options_tab.bindOnlySuccCheckBox(self.only_succ_var, self.on_only_success_check)
        self.only_success_toggle_callback = only_success_toggle_callback

        self.alexa_enab_var = tkinter.IntVar()
        self.alexa_enab_var.set(0)
        self.options_tab.bindAlexaCheckBox(self.alexa_enab_var)

        self.load_img_enabled_var = tkinter.IntVar()
        self.load_img_enabled_var.set(0)
        self.options_tab.bind_load_img_enabled_cb(self.load_img_enabled_var)

        self.locales_enab_var = tkinter.IntVar()
        self.locales_enab_var.set(0)
        self.options_tab.bindLocalesCheckBox(self.locales_enab_var)

        self.proxy_timeout = tkinter.StringVar()
        self.options_tab.bind_proxy_timeout(self.proxy_timeout)

        self.proxy_success_req_min_size = tkinter.StringVar()
        self.options_tab.bind_proxy_succ_req_min_size(self.proxy_success_req_min_size)

        self.proxy_max_fails = tkinter.StringVar()
        self.options_tab.bind_proxy_max_fails(self.proxy_max_fails)

        # Options - js ref injection
        self.use_js_ref_inj = tkinter.IntVar()
        self.use_js_ref_inj.set(1)
        self.options_tab.bindJsInjectCheckBox(self.use_js_ref_inj, None)

        self.js_ref_inj_timeout = tkinter.StringVar()
        self.js_ref_inj_timeout.set('0')
        self.options_tab.bind_js_ref_timeout(self.js_ref_inj_timeout)

        self.options_tab.bind_text_modification(self.on_ui_text_modification)

        self.cookies_enab_var = tkinter.IntVar()
        self.cookies_enab_var.set(0)
        self.options_tab.bind_cookies_checkbox(self.cookies_enab_var)

        self.cookies_file = tkinter.StringVar()
        self.cookies_file.set(default_cookies_file)

        self.options_tab.bind_cookies_file_entry(self.cookies_file)
        self.options_tab.bind_cookies_file_btn(self.on_choose_cookies_file)

        self.enable_similarweb = tkinter.IntVar()
        self.enable_similarweb.set(0)
        self.options_tab.bind_enable_similarweb(self.enable_similarweb)

    ###
    # API
    ###

    def is_alexa_enab_on(self):
        return self.alexa_enab_var.get() == 1

    def set_alexa_enab(self, value: bool):
        self.alexa_enab_var.set(1 if value is True else 0)

    def is_load_img_enabled(self):
        return self.load_img_enabled_var.get() == 1

    def set_load_img_enabled(self, value: bool):
        self.load_img_enabled_var.set(1 if value is True else 0)

    def is_locales_enab_on(self):
        return self.locales_enab_var.get() == 1

    def set_locales_enab(self, value: bool):
        self.locales_enab_var.set(1 if value is True else 0)

    def is_cookies_enab_on(self):
        return self.cookies_enab_var.get() == 1

    def set_cookies_enab(self, value: bool):
        self.cookies_enab_var.set(1 if value is True else 0)

    def getResolutionsText(self):
        return self.options_tab.resolutions_stext.get('0.0', tkinter.END)

    def getResolutionsList(self):
        resolutions_list = self.getResolutionsText().split("\n")
        while resolutions_list.count("") > 0:
            del resolutions_list[resolutions_list.index("")]
        resolutions_list = [x for x in resolutions_list if re.match(r'\d+x\d+', x)]
        return [[int(y) for y in x.split('x')] for x in resolutions_list]

    def get_resolutions_list_as_textlist(self):
        resolutions_list = self.getResolutionsText().split("\n")
        while resolutions_list.count("") > 0:
            del resolutions_list[resolutions_list.index("")]
        resolutions_list = [x for x in resolutions_list if re.match(r'\d+x\d+', x)]
        return resolutions_list

    def setResolutionsText(self, text_str):
        self.options_tab.resolutions_stext.delete('0.0', tkinter.END)
        return self.options_tab.resolutions_stext.insert('0.0', text_str)

    def setResolutionsList(self, re_list):
        str_resolutions = ""
        for res in re_list:
            str_resolutions += str(res[0]) + 'x' + str(res[1]) + "\n"

        self.options_tab.resolutions_stext.delete('0.0', tkinter.END)
        return self.options_tab.resolutions_stext.insert('0.0', str_resolutions)

    def getLocalesList(self):
        locales_list = self.getLocalesText().split("\n")

        while locales_list.count("") > 0:
            del locales_list[locales_list.index("")]

        return locales_list

    def getLocalesText(self):
        return self.options_tab.locales_stext.get('0.0', tkinter.END)

    def setLocalesList(self, locales_list):
        str_locales = ""
        for locale in locales_list:
            str_locales += str(locale) + "\n"

        self.options_tab.locales_stext.delete('0.0', tkinter.END)
        return self.options_tab.locales_stext.insert('0.0', str_locales)

    def setLocalesText(self, text_str):
        self.options_tab.locales_stext.delete('0.0', tkinter.END)
        return self.options_tab.locales_stext.insert('0.0', text_str)

    def is_snapshot_on(self):
        return self.snapshot_var.get() == 1

    def set_snapshot(self, value):
        self.snapshot_var.set(1 if value is True else 0)

    def is_only_success_on(self):
        return self.only_succ_var.get() == 1

    def set_only_success(self, value):
        self.only_succ_var.set(1 if value is True else 0)

    def getMinPageTime(self):
        return float(self.min_pg_time.get())

    def getMaxPageTime(self):
        return float(self.max_pg_time.get())

    def getProxyTimeout(self):
        return int(self.proxy_timeout.get())

    def getProxyMinSuccResponse(self):
        return int(self.proxy_success_req_min_size.get())

    def getProxyMaxFails(self):
        return int(self.proxy_max_fails.get())

    def getUseJsRefInj(self):
        return self.use_js_ref_inj.get() == 1

    def getJsRefInjTimeout(self):
        return int(self.js_ref_inj_timeout.get())

    def getAfterScriptWait(self):
        return float(self.after_script_wait.get())

    def get_cookies_file(self):
        return self.cookies_file.get()

    def set_cookies_file(self, value: str):
        self.cookies_file.set(value)

    def get_enable_similarweb(self):
        return self.enable_similarweb.get()== 1

    def set_enable_similarweb(self, value: bool):
        self.enable_similarweb.set(1 if value is True else 0)

    def setMinPageTime(self, val):
        self.min_pg_time.set(str(val))

    def setMaxPageTime(self, val):
        self.max_pg_time.set(str(val))

    def setProxyTimeout(self, val):
        self.proxy_timeout.set(str(val))

    def setProxyMinSuccessResponse(self, val):
        self.proxy_success_req_min_size.set(str(val))

    def setProxyMaxFails(self, val):
        self.proxy_max_fails.set(str(val))

    def setUseJsRefInj(self, val):
        self.use_js_ref_inj.set(1 if val is True else 0)

    def setJsRefInjTimeout(self, val):
        self.js_ref_inj_timeout.set(str(val))

    def setAfterScriptWait(self, val):
        self.after_script_wait.set(str(val))

    ###
    # Callbacks
    ###

    def on_snapshot_check(self):
        if self.snapshot_toggle_callback is not None:
            self.snapshot_toggle_callback()

    def on_only_success_check(self):
        if self.only_success_toggle_callback is not None:
            self.only_success_toggle_callback()

    def on_ui_text_modification(self, event: tkinter.Event):
        ignore_keys = [16, 17, 18, 20, 27, 33, 34, 35, 36, 37, 38, 39, 40, 45, 91, 112, 113, 114, 115, 116, 117, 118,
                       119,  120, 121, 122, 123]
        if event.keycode not in ignore_keys:
            self.ui_data_changed()

    def on_choose_cookies_file(self):
        filename = openFilenameDial('Load the cookies file')
        if filename:
            self.cookies_file.set(filename)
