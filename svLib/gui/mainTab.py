from tkinter import ttk, Frame, Label, Button, font, LabelFrame, Checkbutton, Radiobutton, Spinbox, Entry, Text, N, \
    S, W, E, END

from svLib import globalConstants
from svLib.gui.components.toolTip import ListboxToolTip
import svLib.gui.helpers as gui_helpers


class MainTab:
    def __init__(self, note_book, b_start_callback, b_stop_callback, update_drivers_command):
        self.checkBoxOn_clr = "#109c1b"
        self.checkBoxOff_clr = "#ff0000"
        self.checkBoxOn_txt = globalConstants.MAIN_TAB_CHCK_ON
        self.checkBoxOff_txt = globalConstants.MAIN_TAB_CHCK_OFF
        self.svg_listboxHighlighted_clr = '#fba521'
        self.svg_listboxUnlighted_clr = '#13ea7f'

        self.fg_param_str = 'foreground'

        self.tab_main = ttk.Frame(note_book)
        note_book.add(self.tab_main, text=globalConstants.MAIN_TAB_TAB_NAME)

        parent_frame = self.tab_main

        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        # Top frame with website name and visits setting
        self.topSection(parent_frame, update_drivers_command)

        # Mid frame, all the proxy, UA, referral lists
        self.midSectionCreation(parent_frame)

        # Bottom frame, start/stop. progress bar
        self.bottomSection(parent_frame, b_start_callback, b_stop_callback)

    ###
    # Design and setup
    ###

    def topSection(self, parent_frame, update_drivers_command):
        top_text_frame = LabelFrame(parent_frame, text=globalConstants.MAIN_TAB_TARG_OPTIONS)
        top_text_frame.grid(row=0, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)
        top_text_frame.grid_rowconfigure(0, weight=1)
        top_text_frame.grid_columnconfigure(0, weight=1)

        # the first row - web address, threads, etc
        url_part = Frame(top_text_frame)
        url_part.grid(row=0, column=0, sticky=W + E + S + N)
        url_part.grid_rowconfigure(0, weight=1)
        url_part.grid_columnconfigure(1, weight=1)

        Label(url_part, text=globalConstants.MAIN_TAB_WEBSITES_TXT).grid(row=0, column=0)
        self.web_site_text = Text(url_part, width=100, undo=True, height=4,
                                  font=font.Font(family='Helvetica', size=8))
        self.web_site_text.grid(row=0, column=1, sticky=W + E)

        config_part = Frame(top_text_frame)
        config_part.grid(row=0, column=1, padx=4)

        Label(config_part, text=globalConstants.MAIN_TAB_VISITS).grid(row=0, column=0, pady=4)
        self.visits_en = Entry(config_part, width=14)
        self.visits_en.grid(row=0, column=1, pady=4)

        Label(config_part, text=globalConstants.MAIN_TAB_THREADS).grid(row=1, column=0, pady=4)
        self.threads_sb = Spinbox(config_part, from_=0, to=99, width=12)
        self.threads_sb.grid(row=1, column=1, pady=4)
        ListboxToolTip(self.threads_sb, [globalConstants.MAIN_TAB_THREADS_HINT_1,
                                         globalConstants.MAIN_TAB_THREADS_HINT_2], 30, 2)

        # row #2: browser choice and update drivers BTN
        self.top_switch_frame = Frame(top_text_frame)
        self.top_switch_frame.grid(row=1, column=0, columnspan=1, sticky=W)
        lbl_br = Label(self.top_switch_frame, text=globalConstants.MAIN_TAB_BROWSER)
        lbl_br.grid(row=0, column=0)
        ListboxToolTip(lbl_br,
                       [globalConstants.MAIN_TAB_BROWSER_HINT_1,
                        globalConstants.MAIN_TAB_BROWSER_HINT_2], 45, 2)
        self.browsers_rad_btns = [
            Radiobutton(self.top_switch_frame, text=globalConstants.BR_PJS, value=globalConstants.BR_PJS),
            Radiobutton(self.top_switch_frame, text=globalConstants.BR_CHR, value=globalConstants.BR_CHR),
            Radiobutton(self.top_switch_frame, text=globalConstants.BR_FX, value=globalConstants.BR_FX)
        ]
        ListboxToolTip(self.browsers_rad_btns[2],
                       [globalConstants.MAIN_TAB_FF_NIGHTLY_HINT_2], 40, 1)

        browser_buttons_count = 1
        for browser_buttons_count in range(1, len(self.browsers_rad_btns) + 1):
            self.browsers_rad_btns[browser_buttons_count - 1].grid(row=0, column=browser_buttons_count)

        self.update_drivers_btn = Button(self.top_switch_frame, text=globalConstants.MAIN_TAB_UPD_DRIVERS,
                                         command=update_drivers_command,
                                         font=font.Font(family="Courier New", size=10, weight="bold"), fg='#0a7212')
        self.update_drivers_btn.grid(row=0, column=browser_buttons_count + 1, sticky=N + S + W + E)
        self.prox_load_tip = ListboxToolTip(self.update_drivers_btn,
                                            [globalConstants.MAIN_TAB_UPD_DRIVERS_HINT_1,
                                             globalConstants.MAIN_TAB_UPD_DRIVERS_HINT_2,
                                             globalConstants.MAIN_TAB_UPD_DRIVERS_HINT_3], 50, 3)

        # row #3: browser options
        self.br_config_fr = Frame(top_text_frame)

        self.headless_mode_chk = Checkbutton(self.br_config_fr, text=globalConstants.MAIN_TAB_HEADLESS)
        ListboxToolTip(self.headless_mode_chk,
                       [globalConstants.MAIN_TAB_HEADLESS_HINT_1,
                        globalConstants.MAIN_TAB_HEADLESS_HINT_2,
                        globalConstants.MAIN_TAB_HEADLESS_HINT_3], 30, 3)
        self.hide_offscreen_chk = Checkbutton(self.br_config_fr, text=globalConstants.MAIN_TAB_HIDE_OFF_SCREEN)
        ListboxToolTip(self.hide_offscreen_chk,
                       [globalConstants.MAIN_TAB_HIDE_OFF_SCREEN_HINT_1,
                        globalConstants.MAIN_TAB_HIDE_OFF_SCREEN_HINT_2,
                        globalConstants.MAIN_TAB_HIDE_OFF_SCREEN_HINT_3], 55, 3)

        self.br_config_fr.grid(row=2, column=0, columnspan=2, sticky=W)
        lbl_brows_path = Label(self.br_config_fr, text=globalConstants.MAIN_TAB_BROWSER_PATH)
        ListboxToolTip(lbl_brows_path,
                       [globalConstants.MAIN_TAB_BROWSER_PATH_HINT], 30, 1)
        self.entry_brows_path = Entry(self.br_config_fr, width=100)
        ListboxToolTip(self.entry_brows_path,
                       [globalConstants.MAIN_TAB_BROWSER_PATH_EF_HINT_1,
                        globalConstants.MAIN_TAB_BROWSER_PATH_EF_HINT_2,
                        globalConstants.MAIN_TAB_BROWSER_PATH_EF_HINT_3], 55, 3)

        self.headless_mode_chk.grid(row=0, column=0, sticky=W)
        self.hide_offscreen_chk.grid(row=0, column=1, sticky=W)
        lbl_brows_path.grid(row=0, column=2, sticky=W)
        self.entry_brows_path.grid(row=0, column=3, sticky=W)

    def midSectionCreation(self, parent_frame):
        mid1_frame = LabelFrame(parent_frame, text=globalConstants.MAIN_TAB_REQ_OPTIONS)
        mid1_frame.grid(row=1, column=0, sticky=N + S + W + E, padx=4, pady=4, ipady=4)
        mid1_frame.grid_rowconfigure(0, weight=1)
        mid1_frame.grid_columnconfigure(0, weight=1)
        mid1_frame.grid_columnconfigure(1, weight=1)
        mid1_frame.grid_columnconfigure(2, weight=1)

        # scrollable listboxes (referrals, browser agents, proxies
        self.list_box_ref, ref_frame = gui_helpers.makeScrollableListBox(mid1_frame, 0, start_row=1)

        self.list_box_ua, ua_frame = gui_helpers.makeScrollableListBox(mid1_frame, 1, start_row=1)

        self.list_box_proxy, proxy_frame = gui_helpers.makeScrollableListBox(mid1_frame, 2, start_row=1)

        ref_frame.grid_rowconfigure(1, weight=1)
        ref_frame.grid_columnconfigure(0, weight=1)
        ref_frame.grid(sticky=W + E + S + N)

        ua_frame.grid_rowconfigure(1, weight=1)
        ua_frame.grid_columnconfigure(0, weight=1)
        ua_frame.grid(sticky=W + E + S + N)

        proxy_frame.grid_rowconfigure(1, weight=1)
        proxy_frame.grid_columnconfigure(0, weight=1)
        proxy_frame.grid(sticky=W + E + S + N)

        # buttons (to load the lists of thereof)
        fb1 = Frame(ref_frame)
        fb1.grid(row=3, column=0, sticky=N + S + W + E)
        fb1.grid_rowconfigure(0, weight=1)
        fb1.grid_columnconfigure(0, weight=1)
        self.b1 = Button(fb1, text=globalConstants.MAIN_TAB_LOAD_REF_LIST)
        self.clr_b1 = Button(fb1, text=globalConstants.MAIN_TAB_CLEAR_REF_LIST)
        self.b1.grid(row=0, column=0, sticky=N + S + W + E)
        self.clr_b1.grid(row=0, column=1, sticky=N + S + W + E)

        fb2 = Frame(ua_frame)
        fb2.grid(row=3, column=0, sticky=N + S + W + E)
        fb2.grid_rowconfigure(0, weight=1)
        fb2.grid_columnconfigure(0, weight=1)
        self.b2 = Button(fb2, text=globalConstants.MAIN_TAB_LOAD_AGENT_LIST)
        self.clr_b2 = Button(fb2, text=globalConstants.MAIN_TAB_CLEAR_AGENT_LIST)
        self.b2.grid(row=0, column=0, sticky=N + S + W + E)
        self.clr_b2.grid(row=0, column=1, sticky=N + S + W + E)

        fb3 = Frame(proxy_frame)
        fb3.grid(row=3, column=0, sticky=N + S + W + E)
        fb3.grid_rowconfigure(0, weight=1)
        fb3.grid_columnconfigure(0, weight=1)
        self.b3 = Button(fb3, text=globalConstants.MAIN_TAB_LOAD_PROXY_LIST)
        self.clr_b3 = Button(fb3, text=globalConstants.MAIN_TAB_CLEAR_PROXY_LIST)
        self.b3.grid(row=0, column=0, sticky=N + S + W + E)
        self.prox_load_tip = ListboxToolTip(self.b3,
                                            [globalConstants.MAIN_TAB_LOAD_PROXY_HINT_1,
                                             globalConstants.MAIN_TAB_LOAD_PROXY_HINT_2,
                                             globalConstants.MAIN_TAB_LOAD_PROXY_HINT_3], 46, 3)

        self.clr_b3.grid(row=0, column=1, sticky=N + S + W + E)
        self.prox_test_btn = Button(fb3, text=globalConstants.MAIN_TAB_TEST_PROXIES, fg='#1072ca')
        self.prox_test_btn.grid(row=0, column=2, sticky=N + S + W + E)
        self.prox_tst_tip = ListboxToolTip(self.prox_test_btn,
                                           [globalConstants.MAIN_TAB_TEST_PROXIES_HINT_1,
                                            globalConstants.MAIN_TAB_TEST_PROXIES_HINT_2,
                                            globalConstants.MAIN_TAB_TEST_PROXIES_HINT_3], 50, 3)

        # Labels, on top, explain shit, activation checkboxes
        _, self.ref_max, self.cb1 = gui_helpers.label4CheckBoxHeader(ref_frame, globalConstants.MAIN_TAB_REFERERS,
                                                                     self.checkBoxOn_txt,
                                                                     self.checkBoxOn_clr)
        _, self.ua_max, self.cb2 = gui_helpers.label4CheckBoxHeader(ua_frame, globalConstants.MAIN_TAB_UAS,
                                                                    self.checkBoxOn_txt,
                                                                    self.checkBoxOn_clr)
        self.prox_curr, self.prox_max, self.cb3 = gui_helpers.label4CheckBoxHeader(proxy_frame,
                                                                                   globalConstants.MAIN_TAB_PROXIES,
                                                                                   self.checkBoxOn_txt,
                                                                                   self.checkBoxOn_clr, True)

    def bottomSection(self, parent_frame, b_start_callback, b_stop_callback):
        bot_frame = LabelFrame(parent_frame, text=globalConstants.MAIN_TAB_VISITS_PROGRESS)
        bot_frame.grid(row=2, column=0, sticky=N + S + W + E, padx=4, pady=4)

        # buttons to start/stop the process
        self.start_btn = Button(bot_frame, text=globalConstants.MAIN_TAB_START, command=b_start_callback,
                                font=font.Font(family="Impact", size=22), fg='#0a7212')
        self.start_btn.grid(row=0, column=0, sticky=N + S + W + E, padx=5, pady=7)
        self.stop_btn = Button(bot_frame, text=globalConstants.MAIN_TAB_STOP, command=b_stop_callback,
                               font=font.Font(family="Impact", size=22), fg='#c53434')
        self.stop_btn.grid(row=0, column=1, sticky=N + S + W + E, padx=5, pady=7)

        # progress bar
        self.pb1 = ttk.Progressbar(bot_frame, orient='horizontal', mode='determinate', length=550, maximum=100)
        self.pb1.grid(row=0, column=3, sticky=N + S + W + E, padx=5, pady=7)

        # progress texts
        bot_txts_frame = Frame(bot_frame)
        bot_txts_frame.grid(row=0, column=4, padx=5, pady=7)
        Label(bot_txts_frame, text=globalConstants.MAIN_TAB_VISITS_2, fg='#01d46d').grid(row=0, column=0)
        self.visits_made_lab = Label(bot_txts_frame, text="0", fg='#01d46d')
        self.visits_made_lab.grid(row=0, column=1)
        Label(bot_txts_frame, text=globalConstants.MAIN_TAB_THREADS_2, fg='#4675c5').grid(row=1, column=0)
        self.threads_act_lab = Label(bot_txts_frame, text="0", fg='#4675c5')
        self.threads_act_lab.grid(row=1, column=1)

    ###
    # Callbacks and API
    ####

    def refOn(self):
        self.cb1.config(text=self.checkBoxOn_txt, fg=self.checkBoxOn_clr)

    def refOff(self):
        self.cb1.config(text=self.checkBoxOff_txt, fg=self.checkBoxOff_clr)

    def uaOn(self):
        self.cb2.config(text=self.checkBoxOn_txt, fg=self.checkBoxOn_clr)

    def uaOff(self):
        self.cb2.config(text=self.checkBoxOff_txt, fg=self.checkBoxOff_clr)

    def proxyOn(self):
        self.cb3.config(text=self.checkBoxOn_txt, fg=self.checkBoxOn_clr)

    def proxyOff(self):
        self.cb3.config(text=self.checkBoxOff_txt, fg=self.checkBoxOff_clr)

    def getLBReferrerContents(self):
        return self.list_box_ref.get(0, self.list_box_ref.size())

    def getLBUAContents(self):
        return self.list_box_ua.get(0, self.list_box_ua.size())

    def getLBProxyContents(self):
        return self.list_box_proxy.get(0, self.list_box_proxy.size())

    def insertListBoxRef(self, string):
        self.list_box_ref.insert(END, string)

    def insertListBoxUa(self, string):
        self.list_box_ua.insert(END, string)

    def insertListBoxProxy(self, string):
        self.list_box_proxy.insert(END, string)

    def clearListBoxRef(self):
        self.list_box_ref.delete(0, END)

    def clearListBoxUa(self):
        self.list_box_ua.delete(0, END)

    def clearListBoxProxy(self):
        self.list_box_proxy.delete(0, END)

    def getListBoxRefSize(self):
        return self.list_box_ref.size()

    def getListBoxUaSize(self):
        return self.list_box_ua.size()

    def getListBoxProxySize(self):
        return self.list_box_proxy.size()

    def getListBoxRefVal(self, index):
        return self.list_box_ref.get(index)

    def getListBoxUaVal(self, index):
        return self.list_box_ua.get(index)

    def getListBoxProxyVal(self, index):
        return self.list_box_proxy.get(index)

    def isRefHighlited(self, index):
        return self.list_box_ref.itemcget(index, self.fg_param_str) == self.svg_listboxUnlighted_clr

    def isRefUnhighlited(self, index):
        return self.list_box_ref.itemcget(index, self.fg_param_str) == self.svg_listboxHighlighted_clr

    def isUAHighlited(self, index):
        return self.list_box_ua.itemcget(index, self.fg_param_str) == self.svg_listboxUnlighted_clr

    def isUAUnhighlited(self, index):
        return self.list_box_ua.itemcget(index, self.fg_param_str) == self.svg_listboxHighlighted_clr

    def isProxyHighlited(self, index):
        return self.list_box_proxy.itemcget(index, self.fg_param_str) == self.svg_listboxUnlighted_clr

    def isProxyUnhighlited(self, index):
        return self.list_box_proxy.itemcget(index, self.fg_param_str) == self.svg_listboxHighlighted_clr

    def highlightReferral(self, index):
        self.list_box_ref.itemconfig(index, foreground=self.svg_listboxUnlighted_clr,
                                     selectbackground=self.svg_listboxUnlighted_clr)

    def highlightUA(self, index):
        self.list_box_ua.itemconfig(index, foreground=self.svg_listboxUnlighted_clr,
                                    selectbackground=self.svg_listboxUnlighted_clr)

    def highlightProxy(self, index):
        self.list_box_proxy.itemconfig(index, foreground=self.svg_listboxUnlighted_clr,
                                       selectbackground=self.svg_listboxUnlighted_clr)

    def highlightReferralBad(self, index):
        self.list_box_ref.itemconfig(index, foreground=self.svg_listboxHighlighted_clr,
                                     selectbackground=self.svg_listboxHighlighted_clr)

    def highlightUABad(self, index):
        self.list_box_ua.itemconfig(index, foreground=self.svg_listboxHighlighted_clr,
                                    selectbackground=self.svg_listboxHighlighted_clr)

    def highlightProxyBad(self, index):
        self.list_box_proxy.itemconfig(index, foreground=self.svg_listboxHighlighted_clr,
                                       selectbackground=self.svg_listboxHighlighted_clr)

    def scrollListBox1To(self, index):
        self.list_box_ref.see(index)
        self.list_box_ref.selection_clear(0, self.list_box_ref.size())
        self.list_box_ref.selection_set(index)
        self.list_box_ref.activate(index)

    def scrollListBox2To(self, index):
        self.list_box_ua.see(index)
        self.list_box_ua.selection_clear(0, self.list_box_ua.size())
        self.list_box_ua.selection_set(index)
        self.list_box_ua.activate(index)

    def scrollListBox3To(self, index):
        self.list_box_proxy.see(index)
        self.list_box_proxy.selection_clear(0, self.list_box_proxy.size())
        self.list_box_proxy.selection_set(index)
        self.list_box_proxy.activate(index)

    def isBrowserPathEnabled(self):  # is it in the grid? is the config thing shown?
        return len(self.br_config_fr.grid_info()) > 0

    ###
    # ViewModel Bindings
    ###

    def bindRefMax(self, var):
        self.ref_max.config(textvariable=var)

    def bindUaMAx(self, var):
        self.ua_max.config(textvariable=var)

    def bindProxCurrent(self, var):
        self.prox_curr.config(textvariable=var)

    def bindProxMax(self, var):
        self.prox_max.config(textvariable=var)

    def bindLoad1Btn(self, callback):
        self.b1.config(command=callback)

    def bindLoad2Btn(self, callback):
        self.b2.config(command=callback)

    def bindLoad3Btn(self, callback):
        self.b3.config(command=callback)

    def bindClrBtn1(self, callback):
        self.clr_b1.config(command=callback)

    def bindClrBtn2(self, callback):
        self.clr_b2.config(command=callback)

    def bindClrBtn3(self, callback):
        self.clr_b3.config(command=callback)

    def bindChkBox1Var(self, var, callback):
        self.cb1.config(command=callback, variable=var)

    def bindChkBox2Var(self, var, callback):
        self.cb2.config(command=callback, variable=var)

    def bindChkBox3Var(self, var, callback):
        self.cb3.config(command=callback, variable=var)

    def bindProgressBar(self, var):
        self.pb1.config(variable=var)

    def bindMadeVisits(self, var):
        self.visits_made_lab.config(textvariable=var)

    def bindActiveThreads(self, var):
        self.threads_act_lab.config(textvariable=var)

    def bindNThreads(self, variable):
        self.threads_sb.config(textvariable=variable)

    def bindNVisitsVar(self, visits_var):
        self.visits_en.config(textvariable=visits_var)

    def bind_browser_choice_radio_buttons(self, var, command):
        for i in range(len(self.browsers_rad_btns)):
            self.browsers_rad_btns[i].config(variable=var, command=command)

    def bind_hide_offscreen_chk(self, ch_var, callback):
        self.hide_offscreen_chk.config(variable=ch_var, command=callback)

    def bind_headless_mode_chk(self, ch_var, callback):
        self.headless_mode_chk.config(variable=ch_var, command=callback)

    def bind_brows_path(self, var):
        self.entry_brows_path.config(textvariable=var)

    def bindProxTestBtn(self, callback):
        self.prox_test_btn.config(command=callback)
