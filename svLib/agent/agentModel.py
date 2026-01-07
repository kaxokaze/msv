import os
import threading

from svLib import globalConstants


class AgentModel:
    def __init__(self, user_config_folder):
        self.user_config_folder = user_config_folder

        # misc fields
        self.sv_proxy_responses: dict = {}
        self.sva_browser_paths: dict = {
            globalConstants.BR_PJS: 'bin/phantomjs.exe',
            globalConstants.BR_FX: '',
            globalConstants.BR_CHR: '',
        }

        self.sv_proxy_success_callback: callable = None
        self.sv_proxy_fail_callback: callable = None

        self.sv_th_stop_callback: callable = None
        self.sv_th_start_callback: callable = None
        self.sv_th_stop_callback: callable = None

        self.chrome_start_semaphore = threading.Semaphore(1)
        self.firefox_start_semaphore = threading.Semaphore(1)

        # Options with defaults
        self.sva_max_proxy_fails: int = 2

        self.sva_headless_mode: bool = True
        self.sva_timeout_interval: float = 60
        self.sva_locales_enabled: bool = True
        self.sva_hide_offscreen: bool = False
        self.sva_alexa_enabled: bool = False
        self.sva_alexa_enabled: bool = False
        self.images_enabled: bool = True
        self.sva_use_js_ref: bool = True
        self.sva_js_inject_timeout: float = 20
        self.sva_min_page_time: float = 3.
        self.sva_max_page_time: float = 7.
        self.sva_after_script_time: float = 1.
        self.sva_do_snapshots: bool = False
        self.sva_success_page_min_size: float = 1100

        self.sva_window_dims: list = [
            [1280, 700],
            [1280, 650],
            [1650, 960],
            [1650, 940],
            [1920, 960],
            [1920, 1100],
        ]

        self.sva_cookies_enabled: bool = False
        self.cookies_file: str = os.path.join(self.user_config_folder, 'cookies.json')

        self.sva_user_scripts: list = []

        self.sva_locales: list = [
            "en",
            "en-us",
            "ru"
        ]

        self.sva_count_success_only: bool = True

        self.autorandom_clicks_enabled: bool = False
        self.click_link_type: str = globalConstants.AUTO_RANDOM_INTERNAL_LINKS
        self.total_autorandom_clicks: int = 2
        self.autorandom_scroll_enabled: bool = False
        self.auto_scroll_percent: float = 50.
        self.after_scroll_time_min: float = 3.
        self.after_scroll_time_max: float = 15.
        self.over_scroll_time_min: float = 6.
        self.over_scroll_time_max: float = 20.

        self.enable_similarweb: bool = False
        self.similarweb_ex_path: str = "chrome-extension://hoklmmgfnpapgjgcpechhaamimifchmp/panel/panel.html?domain=www.similarweb.com"
