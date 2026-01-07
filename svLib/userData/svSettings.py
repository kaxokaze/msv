import os
import shutil

import svLib
import svLib.agent
from svLib.agent import AgentModel
from svLib.log import svLogger
from svLib.userData import svSettingsSerializer
from svLib.viewModel.optionsTabViewModel import OptionsTabViewModel
from svLib.viewModel.userScriptsTabViewModel import UserScriptsTabViewModel

program_data_folder = os.path.join(os.path.expanduser("~"), 'Mass Site Visitor')
default_cookies_path = os.path.join(program_data_folder, "cookies.json")

# find the default userfolder, and see if the program dir exists already, if not - create and populate
svLogger.log_event('Selected program data directory as', program_data_folder)
scraps_folder = os.path.join(program_data_folder, 'scraps')
data_folder = os.path.join(program_data_folder, 'data')
userconfig_folder = os.path.join(program_data_folder, 'userconfig')
visits_folder = os.path.join(program_data_folder, 'visits')
logs_folder = os.path.join(program_data_folder, 'logs')
if not os.path.exists(program_data_folder):
    os.makedirs(program_data_folder)
if not os.path.exists(scraps_folder):
    os.makedirs(scraps_folder)
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
if not os.path.exists(userconfig_folder):
    os.makedirs(userconfig_folder)
if not os.path.exists(visits_folder):
    os.makedirs(visits_folder)
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)
if not os.path.exists(default_cookies_path):
    try:
        shutil.copyfile("data/cookies.json", default_cookies_path)
    except Exception as e:
        pass    # don't care tbh


MIN_PAGE_TIME = 'min_page_time'
MAX_PAGE_TIME = 'max_page_time'
TIMEOUT_INTERVAL = 'timeout_interval'
SUCCESS_PAGE_MIN_SIZE = 'success_page_min_size'
MAX_PROX_FAILS = 'max_prox_fails'
DO_SNAPSHOTS = 'do_snapshots'
COUNT_SUCCESS_ONLY = 'count_success_only'
USE_JS_REF_INJ = 'use_js_ref_inj'
JS_REF_INJ_TIMEOUT = 'js_ref_inj_timeout'
AFTER_SCRIPT_WAIT = 'after_script_wait'
ENABLE_ALEXA = 'enable_alexa'
ENABLE_IMAGES = 'enable_images'
ENABLE_LOCALES = 'enable_locales'
LOCALES_LIST = 'locales_list'
RESOLUTIONS_LIST = 'resolutions_list'
AUTORANDOM_CLICKS_ENABLED = 'autorandom_clicks_enabled'
CLICK_LINK_TYPE = 'click_link_type'
TOTAL_AUTORANDOM_CLICKS = 'total_autorandom_clicks'
AUTORANDOM_SCROLL_ENABLED = 'autorandom_scroll_enabled'
AUTO_SCROLL_PERCENT = 'auto_scroll_percent'
AFTER_SCROLL_TIME_MIN = 'after_scroll_time_min'
AFTER_SCROLL_TIME_MAX = 'after_scroll_time_max'
OVER_SCROLL_TIME_MIN = 'over_scroll_time_min'
OVER_SCROLL_TIME_MAX = 'over_scroll_time_max'
ENABLE_COOKIES = 'enable_cookies'
COOKIES_FILE = 'cookies_file'
ENABLE_SIMILARWEB = 'enable_similarweb'
SIMILARWEB_EX_PATH = 'similarweb_ex_path'


##############################
# Saving/loading the main program Options/Userscripts, etc.
##############################

def set_settings_in_agent(new_settings):
    svLib.agent.set_min_page_time(new_settings.get(MIN_PAGE_TIME))
    svLib.agent.set_max_page_time(new_settings.get(MAX_PAGE_TIME))
    svLib.agent.set_timeout_interval(new_settings.get(TIMEOUT_INTERVAL))
    svLib.agent.set_success_page_min_size(new_settings.get(SUCCESS_PAGE_MIN_SIZE))
    svLib.agent.set_max_prox_fails(new_settings.get(MAX_PROX_FAILS))
    svLib.agent.set_do_snapshots(new_settings.get(DO_SNAPSHOTS))
    svLib.agent.set_count_success_only(new_settings.get(COUNT_SUCCESS_ONLY))
    svLib.agent.set_use_js_ref(new_settings.get(USE_JS_REF_INJ))
    svLib.agent.set_js_inject_timeout(new_settings.get(JS_REF_INJ_TIMEOUT))
    svLib.agent.set_after_script_time(new_settings.get(AFTER_SCRIPT_WAIT))
    svLib.agent.set_alexa(new_settings.get(ENABLE_ALEXA))
    svLib.agent.set_images_enabled(new_settings.get(ENABLE_IMAGES))
    svLib.agent.set_locales_enabled(new_settings.get(ENABLE_LOCALES))
    svLib.agent.set_locales_list(new_settings.get(LOCALES_LIST))
    svLib.agent.set_res_list_from_textlist(new_settings.get(RESOLUTIONS_LIST))
    svLib.agent.set_cookies_enabled(new_settings.get(ENABLE_COOKIES))
    svLib.agent.set_cookies_file(new_settings.get(COOKIES_FILE))
    svLib.agent.set_autorandom_clicks_enabled(new_settings.get(AUTORANDOM_CLICKS_ENABLED))
    svLib.agent.set_click_link_type(new_settings.get(CLICK_LINK_TYPE))
    svLib.agent.set_total_autorandom_clicks(new_settings.get(TOTAL_AUTORANDOM_CLICKS))
    svLib.agent.set_autorandom_scroll_enabled(new_settings.get(AUTORANDOM_SCROLL_ENABLED))
    svLib.agent.set_auto_scroll_percent(new_settings.get(AUTO_SCROLL_PERCENT))
    svLib.agent.set_after_scroll_time_min(new_settings.get(AFTER_SCROLL_TIME_MIN))
    svLib.agent.set_after_scroll_time_max(new_settings.get(AFTER_SCROLL_TIME_MAX))
    svLib.agent.set_over_scroll_time_min(new_settings.get(OVER_SCROLL_TIME_MIN))
    svLib.agent.set_over_scroll_time_max(new_settings.get(OVER_SCROLL_TIME_MAX))
    svLib.agent.set_enable_similarweb(new_settings.get(ENABLE_SIMILARWEB))
    svLib.agent.set_similarweb_ex_path(new_settings.get(SIMILARWEB_EX_PATH))


def load_options(options_viewmodel: OptionsTabViewModel, user_scripts_viewmodel: UserScriptsTabViewModel):
    # program configs
    old_settings, old_resolutions = svSettingsSerializer.parseUserCfgFile(
        os.path.join(program_data_folder, "userconfig", "config.cfg"),
        os.path.join(program_data_folder, "userconfig", "resolutions.cfg")
    )

    new_settings: dict = svSettingsSerializer.parseUserXMLFile(os.path.join(program_data_folder, "userconfig", "config.xml"))

    try:
        if old_resolutions is not None and \
                ((new_settings is None) or (RESOLUTIONS_LIST not in new_settings)):
            if len(old_resolutions) > 0:
                options_viewmodel.setResolutionsText(old_resolutions)
                svLib.agent.set_res_list(options_viewmodel.getResolutionsList())
            else:
                options_viewmodel.setResolutionsList(svLib.agent.get_res_list())

            if new_settings is not None:
                new_settings[RESOLUTIONS_LIST] = options_viewmodel.get_resolutions_list_as_textlist()

        if old_settings is not None and new_settings is None:
            svLib.agent.set_min_page_time(old_settings[MIN_PAGE_TIME])
            svLib.agent.set_max_page_time(old_settings[MAX_PAGE_TIME])
            svLib.agent.set_timeout_interval(old_settings[TIMEOUT_INTERVAL])
            svLib.agent.set_success_page_min_size(old_settings[SUCCESS_PAGE_MIN_SIZE])
            svLib.agent.set_max_prox_fails(old_settings[MAX_PROX_FAILS])
            svLib.agent.set_do_snapshots(old_settings[DO_SNAPSHOTS])
            svLib.agent.set_count_success_only(old_settings[COUNT_SUCCESS_ONLY])
            svLib.agent.set_use_js_ref(old_settings[USE_JS_REF_INJ])
            svLib.agent.set_js_inject_timeout(old_settings[JS_REF_INJ_TIMEOUT])
            svLib.agent.set_after_script_time(old_settings[AFTER_SCRIPT_WAIT])
            svLib.agent.set_alexa(old_settings[ENABLE_ALEXA])
        elif new_settings is not None:
            set_settings_in_agent(new_settings)
    except Exception as e:
        svLogger.log_error('Parsing settings failed:', e)

    pass_agent_config_to_vm(options_viewmodel, user_scripts_viewmodel)

    # user defined scripts
    load_userscripts(user_scripts_viewmodel)


def save_options(options_viewmodel: OptionsTabViewModel, user_scripts_viewmodel: UserScriptsTabViewModel):
    # gets data from gui, sets it in the Visitor Agent module
    user_data = {
        MIN_PAGE_TIME: options_viewmodel.getMinPageTime(),
        MAX_PAGE_TIME: options_viewmodel.getMaxPageTime(),
        TIMEOUT_INTERVAL: options_viewmodel.getProxyTimeout(),
        SUCCESS_PAGE_MIN_SIZE: options_viewmodel.getProxyMinSuccResponse(),
        MAX_PROX_FAILS: options_viewmodel.getProxyMaxFails(),
        DO_SNAPSHOTS: options_viewmodel.is_snapshot_on(),
        COUNT_SUCCESS_ONLY: options_viewmodel.is_only_success_on(),
        USE_JS_REF_INJ: options_viewmodel.getUseJsRefInj(),
        JS_REF_INJ_TIMEOUT: options_viewmodel.getJsRefInjTimeout(),
        AFTER_SCRIPT_WAIT: options_viewmodel.getAfterScriptWait(),
        ENABLE_ALEXA: options_viewmodel.is_alexa_enab_on(),
        ENABLE_IMAGES: options_viewmodel.is_load_img_enabled(),
        ENABLE_LOCALES: options_viewmodel.is_locales_enab_on(),
        LOCALES_LIST: options_viewmodel.getLocalesList(),
        RESOLUTIONS_LIST: options_viewmodel.get_resolutions_list_as_textlist(),
        ENABLE_COOKIES: options_viewmodel.is_cookies_enab_on(),
        COOKIES_FILE: options_viewmodel.get_cookies_file(),
        ENABLE_SIMILARWEB: options_viewmodel.get_enable_similarweb(),
        SIMILARWEB_EX_PATH:  svLib.agent.get_similarweb_ex_path(),
        AUTORANDOM_CLICKS_ENABLED: user_scripts_viewmodel.is_autorandom_clicks_enabled(),
        CLICK_LINK_TYPE: user_scripts_viewmodel.get_click_link_type(),
        TOTAL_AUTORANDOM_CLICKS: user_scripts_viewmodel.get_total_autorandom_clicks(),
        AUTORANDOM_SCROLL_ENABLED: user_scripts_viewmodel.is_autorandom_scroll_enabled(),
        AUTO_SCROLL_PERCENT: user_scripts_viewmodel.get_auto_scroll_percent(),
        AFTER_SCROLL_TIME_MIN: user_scripts_viewmodel.get_after_scroll_time_min(),
        AFTER_SCROLL_TIME_MAX: user_scripts_viewmodel.get_after_scroll_time_max(),
        OVER_SCROLL_TIME_MIN: user_scripts_viewmodel.get_over_scroll_time_min(),
        OVER_SCROLL_TIME_MAX: user_scripts_viewmodel.get_over_scroll_time_max(),
    }
    set_settings_in_agent(user_data)

    # gets userscript from gui, sets them in the Visitor Agent module
    user_scripts = user_scripts_viewmodel.get_user_scripts_for_agent()
    svLib.agent.set_user_scripts(user_scripts)

    # dumps the saves into configfile
    svSettingsSerializer.serializeUserXMLFile(os.path.join(program_data_folder, "userconfig", "config.xml"), user_data)

    # dumps the userscripts into configfile
    svSettingsSerializer.serializeScriptsFile(os.path.join(program_data_folder, "userconfig", "userscripts.cfg"), user_scripts)


def reset_settings_to_defaults(options_tab_vm: OptionsTabViewModel, user_scripts_viewmodel: UserScriptsTabViewModel):
    default_settings: AgentModel = svLib.agent.get_settings_defaults()

    options_tab_vm.setMinPageTime(default_settings.sva_min_page_time)
    options_tab_vm.setMaxPageTime(default_settings.sva_max_page_time)
    options_tab_vm.setProxyTimeout(default_settings.sva_timeout_interval)
    options_tab_vm.setProxyMinSuccessResponse(default_settings.sva_success_page_min_size)
    options_tab_vm.setProxyMaxFails(default_settings.sva_max_proxy_fails)
    options_tab_vm.set_snapshot(default_settings.sva_do_snapshots)
    options_tab_vm.set_only_success(default_settings.sva_count_success_only)
    options_tab_vm.setUseJsRefInj(default_settings.sva_use_js_ref)
    options_tab_vm.setJsRefInjTimeout(default_settings.sva_js_inject_timeout)
    options_tab_vm.setAfterScriptWait(default_settings.sva_after_script_time)
    options_tab_vm.set_alexa_enab(default_settings.sva_alexa_enabled)
    options_tab_vm.set_load_img_enabled(default_settings.images_enabled)
    options_tab_vm.set_locales_enab(default_settings.sva_locales_enabled)
    options_tab_vm.setLocalesList(default_settings.sva_locales)
    options_tab_vm.setResolutionsList(default_settings.sva_window_dims)
    options_tab_vm.set_cookies_enab(default_settings.sva_cookies_enabled)
    options_tab_vm.set_cookies_file(default_settings.cookies_file)
    options_tab_vm.set_enable_similarweb(default_settings.enable_similarweb)
    user_scripts_viewmodel.set_autorandom_clicks_enabled(default_settings.autorandom_clicks_enabled)
    user_scripts_viewmodel.set_click_link_type(default_settings.click_link_type)
    user_scripts_viewmodel.set_total_autorandom_clicks(default_settings.total_autorandom_clicks)
    user_scripts_viewmodel.set_autorandom_scroll_enabled(default_settings.autorandom_scroll_enabled)
    user_scripts_viewmodel.set_auto_scroll_percent(default_settings.auto_scroll_percent)
    user_scripts_viewmodel.set_after_scroll_time_min(default_settings.after_scroll_time_min)
    user_scripts_viewmodel.set_after_scroll_time_max(default_settings.after_scroll_time_max)
    user_scripts_viewmodel.set_over_scroll_time_min(default_settings.over_scroll_time_min)
    user_scripts_viewmodel.set_over_scroll_time_max(default_settings.over_scroll_time_max)


# Passes the Viewer Agent values of the config globals to the gui model.
# Rally can set to defaults only if none of the globals had their values changed sometime during runtime
# before this call. But it's good enough for now
def pass_agent_config_to_vm(options_tab_vm: OptionsTabViewModel, user_scripts_viewmodel: UserScriptsTabViewModel):
    options_tab_vm.setMinPageTime(svLib.agent.get_min_page_time())
    options_tab_vm.setMaxPageTime(svLib.agent.get_max_page_time())
    options_tab_vm.setProxyTimeout(svLib.agent.get_timeout_interval())
    options_tab_vm.setProxyMinSuccessResponse(svLib.agent.get_success_page_min_size())
    options_tab_vm.setProxyMaxFails(svLib.agent.get_max_prox_fails())
    options_tab_vm.set_snapshot(svLib.agent.get_do_snapshots())
    options_tab_vm.set_only_success(svLib.agent.get_count_success_only())
    options_tab_vm.setUseJsRefInj(svLib.agent.get_use_js_ref())
    options_tab_vm.setJsRefInjTimeout(svLib.agent.get_js_inject_timeout())
    options_tab_vm.setAfterScriptWait(svLib.agent.get_after_script_time())
    options_tab_vm.set_alexa_enab(svLib.agent.get_alexa())
    options_tab_vm.set_load_img_enabled(svLib.agent.get_images_enabled())
    options_tab_vm.set_locales_enab(svLib.agent.get_locales_enabled())
    options_tab_vm.setLocalesList(svLib.agent.get_locales_list())
    options_tab_vm.setResolutionsList(svLib.agent.get_res_list())
    options_tab_vm.set_cookies_enab(svLib.agent.get_cookies_enabled())
    options_tab_vm.set_cookies_file(svLib.agent.get_cookies_file())
    options_tab_vm.set_enable_similarweb(svLib.agent.get_enable_similarweb())
    user_scripts_viewmodel.set_autorandom_clicks_enabled(svLib.agent.get_autorandom_clicks_enabled())
    user_scripts_viewmodel.set_click_link_type(svLib.agent.get_click_link_type())
    user_scripts_viewmodel.set_total_autorandom_clicks(svLib.agent.get_total_autorandom_clicks())
    user_scripts_viewmodel.set_autorandom_scroll_enabled(svLib.agent.get_autorandom_scroll_enabled())
    user_scripts_viewmodel.set_auto_scroll_percent(svLib.agent.get_auto_scroll_percent())
    user_scripts_viewmodel.set_after_scroll_time_min(svLib.agent.get_after_scroll_time_min())
    user_scripts_viewmodel.set_after_scroll_time_max(svLib.agent.get_after_scroll_time_max())
    user_scripts_viewmodel.set_over_scroll_time_min(svLib.agent.get_over_scroll_time_min())
    user_scripts_viewmodel.set_over_scroll_time_max(svLib.agent.get_over_scroll_time_max())


def pass_user_scripts_from_agent_to_vm(user_scripts_viewmodel: UserScriptsTabViewModel):
    return user_scripts_viewmodel.set_user_scripts_from_agent(svLib.agent.get_user_scripts())


def reload_userscripts(user_scripts_viewmodel: UserScriptsTabViewModel):
    user_scripts_viewmodel.remove_userscripts()
    load_userscripts(user_scripts_viewmodel)


def load_userscripts(user_scripts_viewmodel: UserScriptsTabViewModel):
    user_scripts = svSettingsSerializer.parseScriptsFile(
        os.path.join(program_data_folder, "userconfig", "userscripts.cfg"))
    for user_script in user_scripts:
        user_scripts_viewmodel.add_user_script_from_settings(user_script)
    svLib.agent.set_user_scripts(user_scripts_viewmodel.get_user_scripts_for_agent())
