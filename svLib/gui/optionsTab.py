import os
from tkinter import Canvas, LabelFrame, Scrollbar, N, S, W, E, Checkbutton, ttk, Spinbox, LEFT, Label, Entry
from tkinter.scrolledtext import ScrolledText

from svLib import globalConstants
from svLib.gui.components.toolTip import ListboxToolTip
from svLib.gui.settingsSaveUi import SettingsSaveUi
from svLib.userData import svSettings
from svLib.utils import guiMouseEvents


class OptionsTab(SettingsSaveUi):
    def __init__(self, note_book, snapshots_folder_open_callback):
        self.tab_options = ttk.Frame(note_book)
        note_book.add(self.tab_options, text=globalConstants.OPTIONS_TAB_NAME)

        self.tab_options.grid_columnconfigure(0, weight=1)
        self.tab_options.grid_rowconfigure(0, weight=1)

        self.options_canvas = Canvas(self.tab_options, bd=0, highlightthickness=0, relief='ridge')
        self.options_canvas.grid(row=0, column=0, sticky=N + S + W + E)
        self.options_canvas.grid_columnconfigure(0, weight=1)
        self.options_canvas.grid_rowconfigure(0, weight=1)
        guiMouseEvents.add_mouse_scroll_to(self.options_canvas)

        # All the code below is just to make it scrollable
        self.options_label_frame = LabelFrame(self.options_canvas, text=globalConstants.OPTIONS_TAB_SETTINGS)
        self.options_label_frame.grid(row=0, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)
        self.options_label_frame.grid_columnconfigure(0, weight=1)
        self.options_label_frame.grid_rowconfigure(0, weight=1)

        v_scrollbar = Scrollbar(self.tab_options)
        v_scrollbar.grid(row=0, column=1, sticky=N + S + W + E)
        v_scrollbar.config(command=self.options_canvas.yview)
        self.options_canvas.config(yscrollcommand=v_scrollbar.set, scrollregion=self.options_canvas.bbox("all"))
        self.options_canvas.create_window((0, 0), window=self.options_label_frame, anchor="nw")

        self.options_label_frame.bind("<Configure>",
                                      lambda e: self.options_canvas.configure(
                                          scrollregion=self.options_canvas.bbox("all")))

        # Visitor Behavior section
        self.vis_behav_section = LabelFrame(self.options_label_frame, text=globalConstants.OPTIONS_TAB_VISITOR_BEHAV)
        self.vis_behav_section.grid(row=0, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)

        # save page snaps checkboxes
        self.snaps_cb = Checkbutton(self.vis_behav_section,
                                    text=globalConstants.OPTIONS_TAB_SAVE_SNAPS + " (" + os.path.join(
                                        svSettings.program_data_folder, 'visits') + ')')
        self.snaps_cb.grid(row=0, column=0, columnspan=1, sticky=W)
        self.open_snapshots_folder_btn = ttk.Button(self.vis_behav_section,
                                                    text=globalConstants.OPTIONS_TAB_OPEN_FOLDER,
                                                    command=snapshots_folder_open_callback)
        self.open_snapshots_folder_btn.grid(row=0, column=1, columnspan=1, sticky=W)

        # count only successes checkbox
        self.success_only_cb = Checkbutton(self.vis_behav_section,
                                           text=globalConstants.OPTIONS_TAB_COUNT_ONLY_SUCC)
        self.success_only_cb.grid(row=1, column=0, columnspan=2, sticky=W)

        # Resolutions sections
        self.br_res_section = LabelFrame(self.options_label_frame,
                                         text=globalConstants.OPTIONS_TAB_BROWSER_RES_LIST)
        self.br_res_section.grid(row=1, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)

        self.resolutions_stext = ScrolledText(self.br_res_section, undo=True, height=4)
        self.resolutions_stext.grid(row=0, column=0, columnspan=2, sticky=W)

        # Proxy health section
        self.proxy_health_frame = LabelFrame(self.options_label_frame, text=globalConstants.OPTIONS_TAB_PROXY_HEALTH)
        self.proxy_health_frame.grid(row=2, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)

        self.prox_timeout_entry = Spinbox(self.proxy_health_frame, from_=0, to=600, width=6)
        self.prox_timeout_entry.grid(row=0, column=0, sticky=W)
        self.prox_succ_req_min_size_entry = Spinbox(self.proxy_health_frame, from_=39, to=100000, width=10)
        self.prox_succ_req_min_size_entry.grid(row=1, column=0, sticky=W)
        self.prox_max_fails_entry = Spinbox(self.proxy_health_frame, from_=0, to=99, width=3)
        self.prox_max_fails_entry.grid(row=2, column=0, sticky=W)

        Label(self.proxy_health_frame, justify=LEFT, text=globalConstants.OPTIONS_TAB_PROXY_TIMEOUT).grid(row=0,
                                                                                                          column=1,
                                                                                                          sticky=W)
        Label(self.proxy_health_frame, justify=LEFT, text=globalConstants.OPTIONS_TAB_PROXY_TIMEOUT_HINT).grid(row=1,
                                                                                                               column=1,
                                                                                                               sticky=W)
        Label(self.proxy_health_frame, justify=LEFT, text=globalConstants.OPTIONS_TAB_MAX_FAILS).grid(
            row=2, column=1, sticky=W)

        # JS referrer injection section
        self.js_ref_section = LabelFrame(self.options_label_frame, text=globalConstants.OPTIONS_TAB_JS_REF_INJ)
        self.js_ref_section.grid(row=3, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)

        self.js_inj_enab_cb = Checkbutton(self.js_ref_section,
                                          text=globalConstants.OPTIONS_TAB_ENABLE_JS_REF_INJ)
        self.js_inj_enab_cb.grid(row=0, column=0, columnspan=2, sticky=W)
        ListboxToolTip(self.js_inj_enab_cb,
                       [globalConstants.OPTIONS_TAB_JS_REF_INJ_HINT_1,
                        globalConstants.OPTIONS_TAB_JS_REF_INJ_HINT_2,
                        globalConstants.OPTIONS_TAB_JS_REF_INJ_HINT_3,
                        globalConstants.OPTIONS_TAB_JS_REF_INJ_HINT_4,
                        globalConstants.OPTIONS_TAB_JS_REF_INJ_HINT_5], 70, 5)

        self.js_inj_timeout_entry = Spinbox(self.js_ref_section, from_=0, to=600, width=6)
        self.js_inj_timeout_entry.grid(row=1, column=0, sticky=W)
        Label(self.js_ref_section, justify=LEFT, text=globalConstants.OPTIONS_TAB_JS_REF_INJ_TIMEOUT).grid(
            row=1, column=1, sticky=W)
        # Additional services section
        self.additional_caps_frame = LabelFrame(self.options_label_frame,
                                                text=globalConstants.OPTIONS_TAB_JS_ADDITIONAL_CAPABILITIES)
        self.additional_caps_frame.grid(row=4, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)

        self.alexa_enab_cb = Checkbutton(self.additional_caps_frame,
                                         text=globalConstants.OPTIONS_TAB_ENABLE_ALEXA)
        self.alexa_enab_cb.grid(row=0, column=0, columnspan=1, sticky=W)
        self.load_img_enabled_cb = Checkbutton(self.additional_caps_frame,
                                               text=globalConstants.OPTIONS_TAB_ENABLE_IMAGES)
        self.load_img_enabled_cb.grid(row=0, column=1, columnspan=1, sticky=W)
        self.enable_similarweb_cb = Checkbutton(self.additional_caps_frame,
                                         text=globalConstants.OPTIONS_TAB_ENABLE_SIMILARWEB)
        self.enable_similarweb_cb.grid(row=1, column=0, columnspan=1, sticky=W)

        # Page visit simulation section
        vis_simul_frame = LabelFrame(self.options_label_frame, text=globalConstants.OPTIONS_TAB_VISIT_SIMULATION)
        vis_simul_frame.grid(row=5, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)

        self.min_pg_time_entry = Spinbox(vis_simul_frame, from_=0, to=12 * 60 * 60, increment=0.5, width=6)
        self.min_pg_time_entry.grid(row=0, column=0, sticky=W)
        self.max_pg_time_entry = Spinbox(vis_simul_frame, from_=0, to=12 * 60 * 60, increment=0.5, width=6)
        self.max_pg_time_entry.grid(row=1, column=0, sticky=W)
        self.after_script_wait_entry = Spinbox(vis_simul_frame, from_=0, to=12 * 60 * 60, increment=0.5, width=6)
        self.after_script_wait_entry.grid(row=2, column=0, sticky=W)

        Label(vis_simul_frame, justify=LEFT, text=globalConstants.OPTIONS_TAB_MIN_STAY_ON_PAGE_INT).grid(row=0,
                                                                                                         column=1,
                                                                                                         sticky=W)
        Label(vis_simul_frame, justify=LEFT, text=globalConstants.OPTIONS_TAB_MAX_STAY_ON_PAGE_INT).grid(row=1,
                                                                                                         column=1,
                                                                                                         sticky=W)
        Label(vis_simul_frame, justify=LEFT,
              text=globalConstants.OPTIONS_TAB_AFTER_SCRIPT_INT).grid(row=2, column=1, sticky=W)

        # Locales
        locale_label_frame = LabelFrame(self.options_label_frame, text=globalConstants.OPTIONS_TAB_LOCALE_LIST)
        locale_label_frame.grid(row=6, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)

        self.locales_enabled_checkbox = Checkbutton(locale_label_frame, text=globalConstants.OPTIONS_TAB_SPOOF_LOCALES)
        self.locales_enabled_checkbox.grid(row=0, column=0, columnspan=1, sticky=W)
        self.locales_stext = ScrolledText(locale_label_frame, undo=True, height=3, width=10)
        self.locales_stext.grid(row=1, column=0, columnspan=1, sticky=W)

        # Locales
        cookie_label_frame = LabelFrame(self.options_label_frame, text=globalConstants.OPTIONS_TAB_COOKIES)
        cookie_label_frame.grid(row=7, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)

        self.cookies_enabled_checkbox = Checkbutton(cookie_label_frame, text=globalConstants.OPTIONS_TAB_ENABLE_COOKIES)
        self.cookies_enabled_checkbox.grid(row=0, column=0, columnspan=3, sticky=W)
        Label(cookie_label_frame, justify=LEFT,
              text=globalConstants.OPTIONS_TAB_COOKIES_FILE).grid(row=1, column=0, sticky=W)
        self.cookies_file_entry = Entry(cookie_label_frame, width=65, state='readonly')
        self.cookies_file_entry.grid(row=1, column=1, padx=1, pady=4, sticky=W)
        self.cookies_file_btn = ttk.Button(cookie_label_frame, text=globalConstants.OPTIONS_TAB_COOKIES_FILE_BUTTON)
        self.cookies_file_btn.grid(row=1, column=2, padx=1, pady=4, sticky=W)

        # Save button
        settings_buttons_frame = ttk.Frame(self.tab_options)
        settings_buttons_frame.grid(row=1, column=0, sticky=W + N + E + S)

        super(OptionsTab, self).__init__(settings_buttons_frame)

    ###
    # ViewModel bindings
    ###

    def bind_cookies_file_entry(self, var):
        self.cookies_file_entry.config(textvariable=var)

    def bind_cookies_file_btn(self, callback):
        self.cookies_file_btn.config(command=callback)

    def bind_cookies_checkbox(self, ch_var, callback=None):
        self.cookies_enabled_checkbox.config(variable=ch_var, command=callback)

    def bind_text_modification(self, on_ui_text_modification):
        self.locales_stext.bind("<KeyPress>", on_ui_text_modification)
        self.resolutions_stext.bind("<KeyPress>", on_ui_text_modification)

    def bindLocalesCheckBox(self, ch_var, callback=None):
        self.locales_enabled_checkbox.config(variable=ch_var, command=callback)

    def bindAlexaCheckBox(self, ch_var, callback=None):
        self.alexa_enab_cb.config(variable=ch_var, command=callback)

    def bind_enable_similarweb(self, ch_var, callback=None):
        self.enable_similarweb_cb.config(variable=ch_var, command=callback)

    def bind_load_img_enabled_cb(self, ch_var, callback=None):
        self.load_img_enabled_cb.config(variable=ch_var, command=callback)

    def bindJsInjectCheckBox(self, ch_var, callback):
        self.js_inj_enab_cb.config(variable=ch_var, command=callback)

    def bind_js_ref_timeout(self, var):
        self.js_inj_timeout_entry.config(textvariable=var)

    def bindSnapCheckBox(self, ch_var, callback):
        self.snaps_cb.config(variable=ch_var, command=callback)

    def bindOnlySuccCheckBox(self, ch_var, callback):
        self.success_only_cb.config(variable=ch_var, command=callback)

    def bind_min_pg_time(self, var):
        self.min_pg_time_entry.config(textvariable=var)

    def bind_max_pg_time(self, var):
        self.max_pg_time_entry.config(textvariable=var)

    def bind_proxy_timeout(self, var):
        self.prox_timeout_entry.config(textvariable=var)

    def bind_proxy_succ_req_min_size(self, var):
        self.prox_succ_req_min_size_entry.config(textvariable=var)

    def bind_proxy_max_fails(self, var):
        self.prox_max_fails_entry.config(textvariable=var)

    def bind_after_script_wait_entry(self, var):
        self.after_script_wait_entry.config(textvariable=var)
