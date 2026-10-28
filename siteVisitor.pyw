import subprocess
import threading
import webbrowser

import os

from svLib import globalConstants, agent
from svLib.agent.visitWorker import VisitWorker
from svLib.drivers import undetectedDriver
from svLib.drivers import driverUpdater
from svLib.gui import mainWindow
from svLib.log import svLogger
import svLib.scraper
from svLib.userData import svSettings
from svLib.viewModel.mainWindowViewModel import MainWindowViewModel


def patch_selenium_and_chromedriver(patch_selenium=True):
    undetectedDriver.install(executable_path=globalConstants.CHROMEDRIVER_PATH, patch_selenium=patch_selenium)


patch_selenium_and_chromedriver()

# For data exchange with visitor threads
sv_sp_sem = threading.Semaphore(1)
sv_fp_sem = threading.Semaphore(1)
sv_s_check_sem = threading.Semaphore(1)

svc_check_w_status = False

svc_check_proxy_suc_que = []

svc_check_proxy_fail_que = []

# For data exchange with scraper thread
svc_received_success_scrap = False
svc_received_failed_scrap = False


#######################
# Callbacks
#######################

def on_frame_update():
    n_visits_completed = agent.getCompletedVisitsNum()
    sv_main_window_model.main_tab_vm.setVisitsMade(n_visits_completed)
    sv_main_window_model.events_tab_vm.set_complete_visits(n_visits_completed)

    if agent.getVisitorTargetTasks() > 0:
        sv_main_window_model.main_tab_vm.setVisitProgress(agent.getVisitorCompletedTasks(),
                                                          agent.getVisitorTargetTasks())
    else:
        sv_main_window_model.main_tab_vm.setVisitProgress(0, 1)

    sv_main_window_model.events_tab_vm.set_all_thread_count(threading.active_count())
    n_wrks = agent.n_workers()
    sv_main_window_model.setThreadsActive(n_wrks)

    sv_main_window_model.events_tab_vm.set_error_cnt(agent.getErrCnt())
    sv_main_window_model.events_tab_vm.set_success_visits(agent.getSuccessCnt())
    sv_main_window_model.events_tab_vm.set_timed_out_cnt(agent.getTimeoutCnt())

    global svc_received_success_scrap
    if svc_received_success_scrap:
        svc_received_success_scrap = False
        enableTheGatherBtn()

    global svc_received_failed_scrap
    if svc_received_failed_scrap:
        svc_received_failed_scrap = False
        enableTheGatherBtn()

    if svc_check_w_status:
        checkoutWorkStatus()

    if len(svc_check_proxy_suc_que) > 0:
        checkoutProxySuccessStatus()

    if len(svc_check_proxy_fail_que) > 0:
        checkoutProxyFailStatus()

    svLogger.step(sv_main_window_model.events_tab_vm)


#################
# Gui callbacks #
#################

# update drivers btn click
def on_update_drivers_click():
    driverUpdater.start_updates_async("bin")
    driverUpdater.updates_finished_callback = lambda: patch_selenium_and_chromedriver(False)


# start btn click
def on_start():
    refs = []
    if sv_main_window_model.main_tab_vm.is_ref_on():
        refs = sv_main_window_model.main_tab_vm.get_ref_list()
    uas = []
    if sv_main_window_model.main_tab_vm.is_ua_on():
        uas = sv_main_window_model.main_tab_vm.get_ua_list()
    proxies = []
    if sv_main_window_model.main_tab_vm.is_proxy_on():
        proxies = sv_main_window_model.main_tab_vm.get_proxy_list()

    sv_main_window_model.events_tab_vm.set_sch_vis(sv_main_window_model.main_tab_vm.get_n_views())

    if sv_main_window_model.main_tab_vm.isBrowserPathEnabled():
        agent.setBrowserPath(sv_main_window_model.main_tab_vm.getBrowserChoice(),
                             sv_main_window_model.main_tab_vm.getBrowserPath())

    url_list = sv_main_window_model.main_tab_vm.get_websites().split('\n')
    try:
        url_list.remove('')
    except:
        pass
    agent.start_visits(url_list, sv_main_window_model.main_tab_vm.get_n_views(), refs, uas, proxies,
                       sv_main_window_model.main_tab_vm.getThreadsMax(),
                       sv_main_window_model.main_tab_vm.getBrowserChoice())


# test proxy btn
def on_test_proxies():
    proxies = []
    if sv_main_window_model.main_tab_vm.is_proxy_on():
        proxies = sv_main_window_model.main_tab_vm.get_proxy_list()

    agent.start_tests(['https://google.com/'], proxies, sv_main_window_model.main_tab_vm.getThreadsMax())


def on_stop():
    if agent.n_workers() > 0 and not (agent.is_scheduler_working() or agent.is_scheduler_testing()):
        agent.purge_visits()
    else:
        agent.cease_visits()


def on_ref_toggle():
    pass


def onUAToggle():
    pass


def onProxyToggle():
    pass


def onSnapshotToggle():
    pass


def browserSwitch():
    if sv_main_window_model.main_tab_vm.isBrowserPathEnabled():
        sv_main_window_model.main_tab_vm.setBrowserPath(
            agent.getBrowserPath(sv_main_window_model.main_tab_vm.getBrowserChoice()))


def headlessModeSwitched():
    agent.setHeadlessMode(sv_main_window_model.main_tab_vm.is_headless_mode_on())


def hideOffscreenSwitched():
    agent.setHideOffscreen(sv_main_window_model.main_tab_vm.is_hide_offscreen_on())


def on_save_options():
    svSettings.save_options(sv_main_window_model.options_tab_vm, sv_main_window_model.user_scripts_tab_vm)


def on_options_discard():
    svSettings.pass_agent_config_to_vm(sv_main_window_model.options_tab_vm, sv_main_window_model.user_scripts_tab_vm)
    scripts_passed = svSettings.pass_user_scripts_from_agent_to_vm(sv_main_window_model.user_scripts_tab_vm)
    if not scripts_passed:
        svSettings.reload_userscripts(sv_main_window_model.user_scripts_tab_vm)


def on_options_reset_default():
    svSettings.reset_settings_to_defaults(sv_main_window_model.options_tab_vm, sv_main_window_model.user_scripts_tab_vm)


def onSnapshotsFolderOpen():
    target_folder = os.path.join(svSettings.program_data_folder, 'visits')
    subprocess.Popen('explorer "%s"' % target_folder)


def onThirdPartyDownloadClicked(event):
    third_party_name = event.widget.cget("text")
    third_party_link = globalConstants.third_party_downloads[third_party_name]
    webbrowser.open_new(third_party_link)


# callbacks from the visitor

def onSuccessfulProxyResp(proxy_addr):
    sv_sp_sem.acquire()

    svc_check_proxy_suc_que.append(proxy_addr)

    sv_sp_sem.release()


def onFailedProxyResp(proxy_addr):
    sv_fp_sem.acquire()

    svc_check_proxy_fail_que.append(proxy_addr)

    sv_fp_sem.release()


def onWorkerStart():
    sv_s_check_sem.acquire()
    global svc_check_w_status
    svc_check_w_status = True
    sv_s_check_sem.release()


def onWorkerStop():
    # Signal the frame handler to refresh status after a worker stops.
    sv_s_check_sem.acquire()
    global svc_check_w_status
    svc_check_w_status = True
    sv_s_check_sem.release()


# Callbacks from the proxy scraper

def onProxyGatherStart():
    svLib.scraper.start_gathering(sv_main_window_model.scrap_proxies_tab_vm.get_current_proxy_provider(),
                                   sv_main_window_model.scrap_proxies_tab_vm.is_http_gather_on(),
                                   sv_main_window_model.scrap_proxies_tab_vm.is_https_gather_on(),
                                   sv_main_window_model.scrap_proxies_tab_vm.is_socks_gather_on(),
                                   sv_main_window_model.scrap_proxies_tab_vm.get_proxy_import_file(),
                                   onProxiesGatherComplete, onProxiesGatherFail,
                                   sv_main_window_model.scrap_proxies_tab_vm.is_transp_gather_on(),
                                   sv_main_window_model.scrap_proxies_tab_vm.is_anon_gather_on(),
                                   sv_main_window_model.scrap_proxies_tab_vm.is_elite_gather_on(),
                                   sv_main_window_model.scrap_proxies_tab_vm.getProxyCountries())

    disableTheGatherBtn()


def onProxyGatherStop():
    svLib.scraper.stop_gathering()
    enableTheGatherBtn()


def onProxiesGatherComplete():
    global svc_received_success_scrap
    svc_received_success_scrap = True

    if sv_main_window_model.scrap_proxies_tab_vm.is_load_rightaway_on():
        try:
            sv_main_window_model.main_tab_vm.preloadProxy(
                open(sv_main_window_model.scrap_proxies_tab_vm.get_proxy_import_file()))
        except Exception as e:
            svLogger.log_error('Immediate loading of the scraped proxies failed somehow:', e)


def onProxiesGatherFail():
    global svc_received_failed_scrap
    svc_received_failed_scrap = True


# helpers for the proxy scraper

def disableTheGatherBtn():
    if sv_main_window_model.scrap_proxies_tab_vm.is_proxy_start_gather_enabled():
        sv_main_window_model.scrap_proxies_tab_vm.state_gathering_stop_proxy_gather_btn()
        sv_main_window_model.scrap_proxies_tab_vm.state_disabled_import_proxy_file_btn()


def enableTheGatherBtn():
    if sv_main_window_model.scrap_proxies_tab_vm.is_proxy_start_gather_gathering():
        sv_main_window_model.scrap_proxies_tab_vm.state_enabled_stop_proxy_gather_btn()
        sv_main_window_model.scrap_proxies_tab_vm.state_enabled_import_proxy_file_btn()


##########################
# Every frame functions, called in enterframe handler
##########################

def checkoutProxyFailStatus():
    sv_fp_sem.acquire()
    proxy_addr = svc_check_proxy_fail_que.pop()
    sv_fp_sem.release()

    proxies = sv_main_window_model.main_tab_vm.get_proxy_list()
    try:  # list might have been changed, maybe the entry just isn't there anymore
        p_ind = proxies.index(proxy_addr)
        # print 'UNHIGHLIGHTING PROXY', p_ind, proxy_addr
        sv_main_window_model.main_tab_vm.highlightProxyBad(p_ind)
    except Exception as e:
        print(e)


def checkoutProxySuccessStatus():
    sv_sp_sem.acquire()
    proxy_addr = svc_check_proxy_suc_que.pop()
    sv_sp_sem.release()

    proxies = sv_main_window_model.main_tab_vm.get_proxy_list()
    # list might have been changed, maybe the entry just isn't there anymore
    try:
        p_ind = proxies.index(proxy_addr)

        if not sv_main_window_model.main_tab_vm.isProxyHighlited(p_ind):
            # print 'HIGHLIGHTING PROXY', p_ind, proxy_addr
            sv_main_window_model.main_tab_vm.set_proxy_count(sv_main_window_model.main_tab_vm.get_proxy_count() + 1)
            sv_main_window_model.main_tab_vm.highlightProxy(p_ind)
    except Exception as e:
        print(e)


def checkoutWorkStatus():
    global svc_check_w_status

    sv_s_check_sem.acquire()
    svc_check_w_status = False
    sv_s_check_sem.release()

    if agent.n_workers() > 0:
        if agent.is_scheduler_testing():
            sv_main_window_model.setTitle("Testing proxies...")
            sv_main_window_model.events_tab_vm.set_vis_status("Testing proxies...")
        elif agent.is_scheduler_working():
            status_str = "Visiting " + agent.current_target_site()[:25] + "..."
            sv_main_window_model.setTitle(status_str)
            sv_main_window_model.events_tab_vm.set_vis_status(status_str)
        else:
            sv_main_window_model.setTitle("Stopping...")
            sv_main_window_model.events_tab_vm.set_vis_status("Stopping...")
    else:
        sv_main_window_model.setTitle('Done.')
        sv_main_window_model.events_tab_vm.set_vis_status('Done.')


##############################
# Entry point
##############################
if __name__ == "__main__":
    # initialize all the objects and whatnot
    sv_main_window = mainWindow.MainWindow(b_start_callback=on_start,
                                           b_stop_callback=on_stop,
                                           on_frame=on_frame_update,
                                           third_party_links=globalConstants.third_party_downloads,
                                           on_third_party_download_clicked=onThirdPartyDownloadClicked,
                                           on_snapshots_folder_open=onSnapshotsFolderOpen,
                                           update_drivers_command=on_update_drivers_click)

    sv_main_window_model = MainWindowViewModel(sv_main_window, VisitWorker.get_link_types(),
                                               svLib.scraper.get_list_of_proxy_dirs(),
                                               on_save_options, on_options_discard, on_options_reset_default,
                                               'http://atomurl.net/myip/', '1000', '10',
                                               ref_callback=on_ref_toggle,
                                               ua_callback=onUAToggle,
                                               proxy_callback=onProxyToggle,
                                               snapshot_toggle_callback=onSnapshotToggle,
                                               start_prox_gather_clk_callback=onProxyGatherStart,
                                               stop_prox_gather_clk_callback=onProxyGatherStop,
                                               default_impor_prx_file=os.path.join(svSettings.program_data_folder,
                                                                                   'data', 'new_proxies.txt'),
                                               br_swit_callback=browserSwitch,
                                               on_hide_offscreen_switch=hideOffscreenSwitched,
                                               test_prox_callback=on_test_proxies,
                                               on_headless_mode_switch=headlessModeSwitched,
                                               on_clear_prox=agent.resetProxyStats,
                                               default_cookies_file=os.path.join(svSettings.program_data_folder,
                                                                                 'cookies.json'))

    sv_main_window.run()
    # kinda initialize it
    hideOffscreenSwitched()
    headlessModeSwitched()

    agent.setListenThreadSuccess(onSuccessfulProxyResp)
    agent.setListenThreadFail(onFailedProxyResp)

    agent.setListenThreadStart(onWorkerStart)
    agent.setListenThreadStop(onWorkerStop)

    svSettings.load_options(sv_main_window_model.options_tab_vm, sv_main_window_model.user_scripts_tab_vm)

    sv_main_window_model.options_tab_vm.bind_change_callback_to_all_vars()
    sv_main_window_model.user_scripts_tab_vm.bind_change_callback_to_all_vars()

    try:
        sv_main_window_model.main_tab_vm.preloadRef(open("data/refs.txt"))
        sv_main_window_model.main_tab_vm.preloadUa(open("data/ua.txt"))
        sv_main_window_model.main_tab_vm.preloadProxy(open("data/proxies.txt"))
    except Exception as exc:
        print(exc)

    sv_main_window.go()

    # this is executed after the window is closed, basically stop all the services, which may or
    # may not be running
    agent.purge_visits(True)
    svLib.scraper.stop_gathering()
