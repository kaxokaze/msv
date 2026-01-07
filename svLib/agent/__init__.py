import re

from svLib.agent.agentModel import AgentModel
from svLib.agent.agentScheduler import AgentScheduler
from svLib.system import childProcessesManager

# Global reference to the settings
from svLib.userData import svSettings

sv_agent_model = AgentModel(svSettings.program_data_folder)
# Global reference to the scheduler
sv_scheduler: AgentScheduler = None


##########################################
# SVAgent API, used to schedule page visits, stop them, get some stats, set some configs, etc
##########################################

def get_settings_defaults():
    return AgentModel(svSettings.program_data_folder)


# an elegant weapon for a more civilised time, will set the alive flag in scheduler to false, that way
# the scheduler will kill every worker from his own thread
def cease_visits():
    if sv_scheduler is not None:
        sv_scheduler.kill()


# a more aggressive approach (this one will basically do the whole thing from the caller-thread, halting it's execution,
# untill all the workers are dealt with)
def purge_visits(purge_ignored_pids=False):
    childProcessesManager.purge_children(purge_ignored=purge_ignored_pids)

    if sv_scheduler is not None:
        sv_scheduler.kill()


def start_visits(website, n_visits, referrers, user_agents, proxies, max_threads, browser):
    cease_visits()

    global sv_scheduler
    sv_scheduler = AgentScheduler(sv_agent_model, website, n_visits, referrers, user_agents, proxies, max_threads,
                                  browser)
    sv_scheduler.startVisits()


def start_tests(website, proxies, max_threads):
    cease_visits()

    global sv_scheduler
    sv_scheduler = AgentScheduler(sv_agent_model, website, -1, None, None, proxies, max_threads, None)
    sv_scheduler.startTests()


def n_workers():
    return sv_scheduler.n_workers() if sv_scheduler is not None else 0


def is_scheduler_working():
    return (sv_scheduler.get_is_alive() and not sv_scheduler.get_is_test_mode()) if sv_scheduler is not None else False


def is_scheduler_testing():
    return (sv_scheduler.get_is_alive() and sv_scheduler.get_is_test_mode()) if sv_scheduler is not None else False


def current_target_site():
    return sv_scheduler.websites[0] if sv_scheduler is not None else ''


def getMadeVisits():
    return sv_scheduler.visits_made if sv_scheduler is not None else 0


def getTotalVisits():
    return sv_scheduler.visits_pending if sv_scheduler is not None else 0


def getCompletedVisitsNum():
    if sv_agent_model.sva_count_success_only:
        return sv_scheduler.getSuccessCnt() if sv_scheduler is not None else 0
    else:
        return sv_scheduler.visits_complete if sv_scheduler is not None else 0


def getVisitorTargetTasks():
    if sv_scheduler is not None and sv_scheduler.get_is_test_mode():
        return sv_scheduler.get_n_loaded_proxies()
    else:
        return getTotalVisits()


def getVisitorCompletedTasks():
    if sv_scheduler is not None and sv_scheduler.get_is_test_mode():
        return sv_scheduler.get_n_loaded_proxies() - len(sv_scheduler.proxies)
    else:
        return getCompletedVisitsNum()


def getSchedulerAlive():
    return sv_scheduler.get_is_alive() if sv_scheduler is not None else 0


def getErrCnt():
    return sv_scheduler.getErrCnt() if sv_scheduler is not None else 0


def getSuccessCnt():
    return sv_scheduler.getSuccessCnt() if sv_scheduler is not None else 0


def getTimeoutCnt():
    return sv_scheduler.getTimeoutCnt() if sv_scheduler is not None else 0


def setListenThreadStart(on_th_start):
    sv_agent_model.sv_th_start_callback = on_th_start


def setListenThreadStop(on_th_stop):
    sv_agent_model.sv_th_stop_callback = on_th_stop


def setListenThreadSuccess(on_prox_succ):
    sv_agent_model.sv_proxy_success_callback = on_prox_succ


def setListenThreadFail(on_prox_fail):
    sv_agent_model.sv_proxy_fail_callback = on_prox_fail


def get_min_page_time():
    return sv_agent_model.sva_min_page_time


def get_max_page_time():
    return sv_agent_model.sva_max_page_time


def get_timeout_interval():
    return sv_agent_model.sva_timeout_interval


def get_success_page_min_size():
    return sv_agent_model.sva_success_page_min_size


def get_max_prox_fails():
    return sv_agent_model.sva_max_proxy_fails


def get_do_snapshots():
    return sv_agent_model.sva_do_snapshots


def get_count_success_only():
    return sv_agent_model.sva_count_success_only


def get_user_scripts():
    return sv_agent_model.sva_user_scripts


def get_use_js_ref():
    return sv_agent_model.sva_use_js_ref


def get_js_inject_timeout():
    return sv_agent_model.sva_js_inject_timeout


def get_after_script_time():
    return sv_agent_model.sva_after_script_time


def set_min_page_time(val: float):
    if val is not None:
        sv_agent_model.sva_min_page_time = val


def set_max_page_time(val: float):
    if val is not None:
        sv_agent_model.sva_max_page_time = val


def set_timeout_interval(val: float):
    if val is not None:
        sv_agent_model.sva_timeout_interval = val


def set_success_page_min_size(val: float):
    if val is not None:
        sv_agent_model.sva_success_page_min_size = val


def set_max_prox_fails(val: int):
    if val is not None:
        sv_agent_model.sva_max_proxy_fails = val


def set_do_snapshots(val: bool):
    if val is not None:
        sv_agent_model.sva_do_snapshots = val == 1


def set_count_success_only(val: bool):
    if val is not None:
        sv_agent_model.sva_count_success_only = val == 1


def set_user_scripts(val):
    sv_agent_model.sva_user_scripts = val


def set_use_js_ref(val: bool):
    if val is not None:
        sv_agent_model.sva_use_js_ref = val


def set_js_inject_timeout(val: float):
    if val is not None:
        sv_agent_model.sva_js_inject_timeout = val


def set_after_script_time(val: float):
    if val is not None:
        sv_agent_model.sva_after_script_time = val


def setBrowserPath(browser, path):
    sv_agent_model.sva_browser_paths[browser] = path


def getBrowserPath(browser):
    return sv_agent_model.sva_browser_paths[browser]


def setHideOffscreen(val: bool):
    if val is not None:
        sv_agent_model.sva_hide_offscreen = val


def setHeadlessMode(val: bool):
    if val is not None:
        sv_agent_model.sva_headless_mode = val


def getHideOffscreen():
    return sv_agent_model.sva_hide_offscreen


def get_res_list():
    return list(sv_agent_model.sva_window_dims)


def set_res_list(res_list: list):
    if res_list is not None and len(res_list) > 0:
        sv_agent_model.sva_window_dims = res_list


def set_res_list_from_textlist(res_text_list: list):
    if res_text_list is not None and len(res_text_list) > 0:
        resolutions_list = [x for x in res_text_list if re.match(r'\d+x\d+', x)]
        res_list = [[int(y) for y in x.split('x')] for x in resolutions_list]
        sv_agent_model.sva_window_dims = res_list


def get_cookies_enabled():
    return sv_agent_model.sva_cookies_enabled


def set_cookies_enabled(val):
    if val is not None:
        sv_agent_model.sva_cookies_enabled = val


def set_cookies_file(cookies_file: str):
    if cookies_file is not None:
        sv_agent_model.cookies_file = cookies_file


def get_cookies_file():
    return sv_agent_model.cookies_file


def get_locales_list():
    return list(sv_agent_model.sva_locales)


def set_locales_list(locales_list):
    if locales_list is not None and len(locales_list) > 0:
        sv_agent_model.sva_locales = locales_list


def resetProxyStats():
    sv_agent_model.sv_proxy_responses = {}


def get_alexa():
    return sv_agent_model.sva_alexa_enabled


def set_alexa(val: bool):
    if val is not None:
        sv_agent_model.sva_alexa_enabled = val


def get_images_enabled():
    return sv_agent_model.images_enabled


def set_images_enabled(val):
    if val is not None:
        sv_agent_model.images_enabled = val


def get_locales_enabled():
    return sv_agent_model.sva_locales_enabled


def set_locales_enabled(val: bool):
    if val is not None:
        sv_agent_model.sva_locales_enabled = val


def set_autorandom_clicks_enabled(param: bool):
    if param is not None:
        sv_agent_model.autorandom_clicks_enabled = param


def get_autorandom_clicks_enabled():
    return sv_agent_model.autorandom_clicks_enabled


def set_click_link_type(param: str):
    if param is not None:
        sv_agent_model.click_link_type = param


def get_click_link_type():
    return sv_agent_model.click_link_type


def set_total_autorandom_clicks(param: int):
    if param is not None:
        sv_agent_model.total_autorandom_clicks = param


def get_total_autorandom_clicks():
    return sv_agent_model.total_autorandom_clicks


def set_autorandom_scroll_enabled(param: bool):
    if param is not None:
        sv_agent_model.autorandom_scroll_enabled = param


def get_autorandom_scroll_enabled():
    return sv_agent_model.autorandom_scroll_enabled


def set_auto_scroll_percent(param: int):
    if param is not None:
        sv_agent_model.auto_scroll_percent = param


def get_auto_scroll_percent():
    return sv_agent_model.auto_scroll_percent


def set_after_scroll_time_min(param: int):
    if param is not None:
        sv_agent_model.after_scroll_time_min = param


def get_after_scroll_time_min():
    return sv_agent_model.after_scroll_time_min


def set_after_scroll_time_max(param: int):
    if param is not None:
        sv_agent_model.after_scroll_time_max = param


def get_after_scroll_time_max():
    return sv_agent_model.after_scroll_time_max


def set_over_scroll_time_min(param: int):
    if param is not None:
        sv_agent_model.over_scroll_time_min = param


def get_over_scroll_time_min():
    return sv_agent_model.over_scroll_time_min


def set_over_scroll_time_max(param: int):
    if param is not None:
        sv_agent_model.over_scroll_time_max = param


def get_over_scroll_time_max():
    return sv_agent_model.over_scroll_time_max


def set_enable_similarweb(param: bool):
    if param is not None:
        sv_agent_model.enable_similarweb = param


def get_enable_similarweb():
    return sv_agent_model.enable_similarweb


def set_similarweb_ex_path(param: str):
    if param is not None:
        sv_agent_model.similarweb_ex_path = param


def get_similarweb_ex_path():
    return sv_agent_model.similarweb_ex_path
