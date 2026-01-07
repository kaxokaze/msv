import tkinter

from svLib import globalConstants
from svLib.utils import stdHelper
from svLib.viewModel.helpers import fillGuiWithFileConts, populateGui


class MainTabViewModel:
    def __init__(self, main_tab, default_website,  default_views, br_swit_callback, default_threads, on_hide_offscreen_switch,
                 on_headless_mode_switch, ref_callback, ua_callback, proxy_callback, test_prox_callback, on_clear_prox):
        self.main_tab = main_tab

        self.set_websites(default_website)

        self.sv_ref_list = []
        self.sv_ua_list = []
        self.sv_proxy_list = []

        self.n_views = tkinter.StringVar()
        self.n_views.set(default_views)
        self.main_tab.bindNVisitsVar(self.n_views)

        # browser choice part of the main tab
        self.browser_choice = tkinter.StringVar()
        self.browser_choice.set(globalConstants.BR_CHR)
        self.browser_switch_callback = br_swit_callback
        self.main_tab.bind_browser_choice_radio_buttons(self.browser_choice, self.on_browser_change)

        self.browser_path = tkinter.StringVar()
        self.main_tab.bind_brows_path(self.browser_path)

        self.is_hide_offscreen = tkinter.IntVar()
        self.main_tab.bind_hide_offscreen_chk(self.is_hide_offscreen, on_hide_offscreen_switch)
        self.is_headless_mode = tkinter.IntVar()
        self.is_headless_mode.set(1)
        self.main_tab.bind_headless_mode_chk(self.is_headless_mode, on_headless_mode_switch)
        # Main tab/window, mid
        self.ref_var = tkinter.IntVar()
        self.ref_var.set(1)
        self.main_tab.refOn()
        self.main_tab.bindChkBox1Var(self.ref_var, self.onRefToggle)
        self.ref_callback = ref_callback

        self.ua_var = tkinter.IntVar()
        self.ua_var.set(1)
        self.main_tab.uaOn()
        self.main_tab.bindChkBox2Var(self.ua_var, self.onUAToggle)
        self.ua_callback = ua_callback

        self.proxy_var = tkinter.IntVar()
        self.proxy_var.set(1)
        self.main_tab.proxyOn()
        self.main_tab.bindChkBox3Var(self.proxy_var, self.onProxyToggle)
        self.proxy_callback = proxy_callback

        self.main_tab.bindClrBtn1(self.clear_ref_callback)
        self.main_tab.bindClrBtn2(self.clear_ua_callback)
        self.main_tab.bindClrBtn3(self.clear_proxy_callback)
        self.prox_clear_cb = on_clear_prox

        self.main_tab.bindLoad1Btn(self.on_load_referral)
        self.main_tab.bindLoad2Btn(self.on_load_ua)
        self.main_tab.bindLoad3Btn(self.on_load_proxy)

        self.ref_max = tkinter.StringVar()
        self.ref_max.set('0')
        self.main_tab.bindRefMax(self.ref_max)

        self.ua_max = tkinter.StringVar()
        self.ua_max.set('0')
        self.main_tab.bindUaMAx(self.ua_max)

        self.proxy_count = tkinter.StringVar()
        self.proxy_count.set('0')
        self.main_tab.bindProxCurrent(self.proxy_count)

        self.proxy_max = tkinter.StringVar()
        self.proxy_max.set('0')
        self.main_tab.bindProxMax(self.proxy_max)

        # test btn
        self.main_tab.bindProxTestBtn(test_prox_callback)

        # Main tab/window, bottom
        self.progress_var = tkinter.IntVar()
        self.main_tab.bindProgressBar(self.progress_var)

        self.visits_made = tkinter.StringVar()
        self.visits_made.set('0')
        self.main_tab.bindMadeVisits(self.visits_made)

        self.active_threads = tkinter.StringVar()
        self.active_threads.set('0')
        self.main_tab.bindActiveThreads(self.active_threads)

        self.max_threads = tkinter.StringVar()
        self.max_threads.set(default_threads)
        self.main_tab.bindNThreads(self.max_threads)

    ################################
    # 'API' of the model
    ################################


    def add_referral(self, ref):
        if stdHelper.addToArray(self.sv_ref_list, ref):
            self.main_tab.insertListBoxRef(ref)

    def add_user_agent(self, ua):
        if stdHelper.addToArray(self.sv_ua_list, ua):
            self.main_tab.insertListBoxUa(ua)

    def add_proxy(self, pr):
        if stdHelper.addToArray(self.sv_proxy_list, pr):
            self.main_tab.insertListBoxProxy(pr)

    def get_n_ref(self):
        return len(self.sv_ref_list)

    def get_n_ua(self):
        return len(self.sv_ua_list)

    def get_n_proxy(self):
        return len(self.sv_proxy_list)

    def get_ref_list(self):
        return self.sv_ref_list

    def get_ua_list(self):
        return self.sv_ua_list

    def get_proxy_list(self):
        return self.sv_proxy_list

    def highlightReferral(self, index):
        self.main_tab.highlightReferral(index)

    def highlightUA(self, index):
        self.main_tab.highlightUA(index)

    def highlightProxy(self, index):
        self.main_tab.highlightProxy(index)

    def highlightReferralBad(self, index):
        self.main_tab.highlightReferralBad(index)

    def highlightUABad(self, index):
        self.main_tab.highlightUABad(index)

    def highlightProxyBad(self, index):
        self.main_tab.highlightProxyBad(index)

    def isRefHighlited(self, index):
        return self.main_tab.isRefHighlited(index)

    def isRefUnhighlited(self, index):
        return self.main_tab.isRefUnhighlited(index)

    def isUAHighlited(self, index):
        return self.main_tab.isUAHighlited(index)

    def isUAUnhighlited(self, index):
        return self.main_tab.isUAUnhighlited(index)

    def isProxyHighlited(self, index):
        return self.main_tab.isProxyHighlited(index)

    def isProxyUnhighlited(self, index):
        return self.main_tab.isProxyUnhighlited(index)

    def get_websites(self):
        return self.main_tab.web_site_text.get('0.0', tkinter.END)

    def set_websites(self, url_str):
        self.main_tab.web_site_text.delete('0.0', tkinter.END)
        self.main_tab.web_site_text.insert('0.0', url_str)

    def get_n_views(self):
        return int(self.n_views.get())

    def is_ref_on(self):
        return self.ref_var.get() == 1

    def is_ua_on(self):
        return self.ua_var.get() == 1

    def is_proxy_on(self):
        return self.proxy_var.get() == 1

    def get_proxy_count(self):
        return int(self.proxy_count.get())

    def set_ref_max(self, val):
        self.ref_max.set(val)

    def set_ua_max(self, val):
        self.ua_max.set(val)

    def set_proxy_count(self, val):
        self.proxy_count.set(val)

    def set_proxy_max(self, val):
        self.proxy_max.set(val)

    def setThreadsMax(self, value):
        self.max_threads.set(str(value))

    def getThreadsMax(self):
        return int(self.max_threads.get())

    def setVisitsMade(self, value):
        self.visits_made.set(str(value))

    def setThreadsActive(self, value):
        self.active_threads.set(str(value))

    def getThreadsActive(self):
        return self.active_threads.get()

    def setVisitProgress(self, value, value_max):
        self.progress_var.set(int(float(value) / float(value_max) * 100))

    def preloadRef(self, r_file):
        fillGuiWithFileConts(r_file, self.add_referral)
        self.set_ref_max(self.get_n_ref())

    def preloadUa(self, u_file):
        fillGuiWithFileConts(u_file, self.add_user_agent)
        self.set_ua_max(self.get_n_ua())

    def preloadProxy(self, p_file):
        fillGuiWithFileConts(p_file, self.add_proxy)
        self.set_proxy_max(self.get_n_proxy())

    def is_hide_offscreen_on(self):
        return self.is_hide_offscreen.get() == 1

    def is_headless_mode_on(self):
        return self.is_headless_mode.get() == 1

    def getBrowserPath(self):
        return self.browser_path.get()

    def setBrowserPath(self, val):
        self.browser_path.set(val)

    def getBrowserChoice(self):
        return self.browser_choice.get()

    def export_healthy_proxies(self, c_file):
        proxies = self.main_tab.getLBProxyContents()

        for i in range(len(proxies)):
            if self.isProxyHighlited(i):
                c_file.write(proxies[i] + '\n')

    def export_non_lagging_proxies(self, c_file):
        proxies = self.main_tab.getLBProxyContents()

        for i in range(len(proxies)):
            if not self.isProxyUnhighlited(i):
                c_file.write(proxies[i] + '\n')

    def isBrowserPathEnabled(self):
        return self.main_tab.isBrowserPathEnabled()
    
    ###
    # Callbacks
    ###

    def on_browser_change(self):
        if self.browser_switch_callback is not None:
            self.browser_switch_callback()

    def clear_ref_callback(self):
        self.sv_ref_list = []
        self.set_ref_max(self.get_n_ref())
        self.main_tab.clearListBoxRef()

    def clear_ua_callback(self):
        self.sv_ua_list = []
        self.set_ua_max(self.get_n_ua())
        self.main_tab.clearListBoxUa()

    def clear_proxy_callback(self):
        self.sv_proxy_list = []
        self.set_proxy_max(self.get_n_proxy())
        self.set_proxy_count(0)
        self.main_tab.clearListBoxProxy()

        if self.prox_clear_cb is not None:
            self.prox_clear_cb()

    def on_load_referral(self):
        populateGui(self.add_referral, "Load referrals from a file")
        self.set_ref_max(self.get_n_ref())

    def on_load_ua(self):
        populateGui(self.add_user_agent, "Load user agents from a file")
        self.set_ua_max(self.get_n_ua())

    def on_load_proxy(self):
        populateGui(self.add_proxy, "Load proxies from a file")
        self.set_proxy_max(self.get_n_proxy())
        self.set_proxy_count(0)

    def onRefToggle(self):
        if self.is_ref_on():
            self.main_tab.refOn()
        else:
            self.main_tab.refOff()

        if self.ref_callback is not None:
            self.ref_callback()

    def onUAToggle(self):
        if self.is_ua_on():
            self.main_tab.uaOn()
        else:
            self.main_tab.uaOff()

        if self.ua_callback is not None:
            self.ua_callback()

    def onProxyToggle(self):
        if self.is_proxy_on():
            self.main_tab.proxyOn()
        else:
            self.main_tab.proxyOff()

        if self.proxy_callback is not None:
            self.proxy_callback()
