from tkinter import ttk, Label, LEFT, E, W, S, N, Checkbutton, Entry, Canvas, LabelFrame, Scrollbar

from svLib import globalConstants
from svLib.gui.components.toolTip import ListboxToolTip
from svLib.utils import guiMouseEvents


class ScrapProxiesTab:
    def __init__(self, note_book, root):
        self.ATTR_TEXT = 'text'

        self.tab_scraping = ttk.Frame(note_book)
        note_book.add(self.tab_scraping, text=globalConstants.SCRAP_TAB_NAME)

        TAB_PADDING = 2
        # row 1
        Label(self.tab_scraping, justify=LEFT, text=globalConstants.SCRAP_TAB_SELECT_SITE).grid(row=0, column=0,
                                                                                                padx=TAB_PADDING,
                                                                                                pady=TAB_PADDING,
                                                                                                sticky=E)
        self.proxy_site_cmbbx = ttk.Combobox(self.tab_scraping, state='readonly', width=30)
        self.proxy_site_cmbbx.grid(row=0, column=1, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)

        self.http_proxy_chkbx = Checkbutton(self.tab_scraping, text="http")
        self.http_proxy_chkbx.grid(row=0, column=2, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)

        self.https_proxy_chkbx = Checkbutton(self.tab_scraping, text="https")
        self.https_proxy_chkbx.grid(row=0, column=3, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)

        self.socks_proxy_chkbx = Checkbutton(self.tab_scraping, text="socks4/5")
        self.socks_proxy_chkbx.grid(row=0, column=4, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)

        # row 2
        self.transparent_proxy_chkbx = Checkbutton(self.tab_scraping, text=globalConstants.SCRAP_TAB_PROXY_TRANSPARENT)
        self.transparent_proxy_chkbx.grid(row=1, column=2, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)

        self.anonymous_proxy_chkbx = Checkbutton(self.tab_scraping, text=globalConstants.SCRAP_TAB_PROXY_ANON)
        self.anonymous_proxy_chkbx.grid(row=1, column=3, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)

        self.elite_proxy_chkbx = Checkbutton(self.tab_scraping, text=globalConstants.SCRAP_TAB_PROXY_ELITE)
        self.elite_proxy_chkbx.grid(row=1, column=4, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)

        # row 3
        Label(self.tab_scraping, justify=LEFT, text=globalConstants.SCRAP_TAB_SAVE_TO).grid(
            row=2, column=0, padx=TAB_PADDING, pady=TAB_PADDING, sticky=E)

        self.import_proxy_to_entry = Entry(self.tab_scraping, width=65, state='readonly')
        self.import_proxy_to_entry.grid(row=2, column=1, padx=1, pady=TAB_PADDING, sticky=W, columnspan=4)

        self.choose_import_proxy_file_btn = ttk.Button(self.tab_scraping, text=globalConstants.SCRAP_TAB_CHOOSE)
        self.choose_import_proxy_file_btn.grid(row=2, column=4, padx=1, pady=TAB_PADDING, sticky=W)

        self.load_rightaway_chk = Checkbutton(self.tab_scraping, text=globalConstants.SCRAP_TAB_LOAD_LIST_INSTANTLY)
        self.prox_imp_tip = ListboxToolTip(self.load_rightaway_chk,
                                           [globalConstants.SCRAP_TAB_LOAD_LIST_INSTANTLY_HINT_1,
                                            globalConstants.SCRAP_TAB_LOAD_LIST_INSTANTLY_HINT_2,
                                            globalConstants.SCRAP_TAB_LOAD_LIST_INSTANTLY_HINT_3,
                                            globalConstants.SCRAP_TAB_LOAD_LIST_INSTANTLY_HINT_4,
                                            globalConstants.SCRAP_TAB_LOAD_LIST_INSTANTLY_HINT_5], 50, 5)

        # row 4
        self.load_rightaway_chk.grid(row=3, column=0, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)

        # row 5: btns for country selection
        self.deselect_countries_btn = ttk.Button(self.tab_scraping,
                                                 text=globalConstants.SCRAP_TAB_DESELECT_ALL_COUNTRIES)
        self.deselect_countries_btn.grid(row=4, column=0, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)
        self.select_countries_btn = ttk.Button(self.tab_scraping, text=globalConstants.SCRAP_TAB_SELECT_ALL_COUNTRIES)
        self.select_countries_btn.grid(row=4, column=1, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)

        # row 6: country selection
        self.country_select_canvas = Canvas(self.tab_scraping, bd=0, highlightthickness=0, relief='ridge')
        self.country_select_canvas.grid(row=5, column=0, columnspan=5, sticky=N + S + W + E)
        self.country_select_canvas.grid_columnconfigure(0, weight=1)
        self.country_select_canvas.grid_rowconfigure(0, weight=1)

        guiMouseEvents.add_mouse_scroll_to(self.country_select_canvas)

        self.country_select_section = LabelFrame(self.country_select_canvas,
                                                 text=globalConstants.SCRAP_TAB_SELECT_COUNTRIES)
        self.country_select_section.grid(row=0, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)
        self.country_select_section.grid_columnconfigure(0, weight=1)
        self.country_select_section.grid_rowconfigure(0, weight=1)
        self.country_select_section.bind("<Configure>", self.onyProxyCountriesFrameConfigure)

        self.last_country_index = 0

        v_scrollbar = Scrollbar(self.tab_scraping)
        v_scrollbar.grid(row=5, column=5, sticky=N + S + W + E)
        v_scrollbar.config(command=self.country_select_canvas.yview)
        self.country_select_canvas.config(yscrollcommand=v_scrollbar.set,
                                          scrollregion=self.country_select_canvas.bbox("all"))
        self.country_select_canvas.create_window((0, 0), window=self.country_select_section, anchor="nw")

        self.country_select_checkboxes = {}

        # row 7
        self.start_style = ttk.Style(root)
        self.start_style.configure('Big.TButton', font=("Impact", 22))

        self.start_proxy_gather_btn = ttk.Button(self.tab_scraping, style='Big.TButton')
        self.state_enabled_stop_proxy_gather_btn()
        self.start_proxy_gather_btn.grid(row=6, column=0, padx=TAB_PADDING, pady=TAB_PADDING, sticky=W)
        self.stop_proxy_gather_btn = ttk.Button(self.tab_scraping, text=globalConstants.SCRAP_TAB_STOP,
                                                style='Big.TButton')
        self.stop_proxy_gather_btn.grid(row=6, column=1, padx=TAB_PADDING, pady=TAB_PADDING, sticky=E)

    ###
    # API
    ###

    def state_enabled_stop_proxy_gather_btn(self):
        self.start_proxy_gather_btn.state(["!disabled"])
        self.start_proxy_gather_btn.config(text=globalConstants.TXT_PRX_START_BTN_ENABLED)

    def state_gathering_stop_proxy_gather_btn(self):
        self.start_proxy_gather_btn.state(["disabled"])
        self.start_proxy_gather_btn.config(text=globalConstants.TXT_PRX_START_BTN_GATHERING)

    def state_stopping_stop_proxy_gather_btn(self):
        self.start_proxy_gather_btn.state(["disabled"])
        self.start_proxy_gather_btn.config(text=globalConstants.TXT_PRX_START_BTN_STOPPING)

    def is_proxy_start_gather_enabled(self):
        return self.start_proxy_gather_btn.cget(self.ATTR_TEXT) == globalConstants.TXT_PRX_START_BTN_ENABLED

    def is_proxy_start_gather_gathering(self):
        return self.start_proxy_gather_btn.cget(self.ATTR_TEXT) == globalConstants.TXT_PRX_START_BTN_GATHERING

    def is_proxy_start_gather_stopping(self):
        return self.start_proxy_gather_btn.cget(self.ATTR_TEXT) == globalConstants.TXT_PRX_START_BTN_STOPPING

    def state_disabled_import_proxy_file_btn(self):
        self.choose_import_proxy_file_btn.state(["disabled"])

    def state_enabled_import_proxy_file_btn(self):
        self.choose_import_proxy_file_btn.state(["!disabled"])

    def onyProxyCountriesFrameConfigure(self, event):
        self.country_select_canvas.configure(scrollregion=self.country_select_canvas.bbox("all"))

    ###
    # ViewModel binding
    ###

    def bind_load_rightaway(self, var):
        self.load_rightaway_chk.config(variable=var)

    def bindImportProxToEntry(self, var):
        self.import_proxy_to_entry.config(textvariable=var)

    def bindChooImportProxFileBtn(self, callback):
        self.choose_import_proxy_file_btn.config(command=callback)

    def bind_proxy_list_cmbbx(self, values: list, var):
        self.proxy_site_cmbbx.config(values=values, textvariable=var)

    def bind_http_chk_btn(self, var, callback):
        self.http_proxy_chkbx.config(command=callback, variable=var)

    def bind_https_chk_btn(self, var, callback):
        self.https_proxy_chkbx.config(command=callback, variable=var)

    def bind_socks_chk_btn(self, var, callback):
        self.socks_proxy_chkbx.config(command=callback, variable=var)

    def bind_transp_chk_btn(self, var, callback):
        self.transparent_proxy_chkbx.config(command=callback, variable=var)

    def bind_anon_chk_btn(self, var, callback):
        self.anonymous_proxy_chkbx.config(command=callback, variable=var)

    def bind_elite_chk_btn(self, var, callback):
        self.elite_proxy_chkbx.config(command=callback, variable=var)

    def bind_start_prox_gather_btn(self, callback):
        self.start_proxy_gather_btn.config(command=callback)

    def bind_stop_prox_gather_btn(self, callback):
        self.stop_proxy_gather_btn.config(command=callback)

    def bindDeselectAllCountriesBtn(self, callback):
        self.deselect_countries_btn.config(command=callback)

    def bindSelectAllCountriesBtn(self, callback):
        self.select_countries_btn.config(command=callback)

    def create_and_bind_country_chk_btn(self, country_code, country_name, var, callback):
        self.country_select_checkboxes[country_code] = Checkbutton(self.country_select_section,
                                                                   text=country_name[:min(len(country_name), 27)])
        self.country_select_checkboxes[country_code].grid(row=int(self.last_country_index / 4),
                                                          column=self.last_country_index % 4, sticky=W)
        self.country_select_checkboxes[country_code].config(command=callback, variable=var)
        self.last_country_index += 1
