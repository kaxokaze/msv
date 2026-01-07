class ScraperModel:
    def __init__(self):
        self.svps_gathered_callback: callable = None
        self.svps_failed_callback: callable = None
        self.svps_proxy_gather_timeout: float = 20
