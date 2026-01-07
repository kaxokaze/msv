class SiteParser:
    SCRAP_LOADING_TIMEOUT = 20

    def __init__(self, site_name, selenium_based):
        self.state = {
            "alive": True,
            "site_name": site_name
        }

        self.uses_selenium = selenium_based

    def scrapProxies(self, do_http, do_https, do_socks, import_target, do_transp, do_anon, do_elite, country_list):
        pass

    def kill(self):
        self.state["alive"] = False

    def setAlive(self, value):
        self.state["alive"] = value

    def isAlive(self):
        return self.state["alive"]

    def getSiteUrl(self):
        return self.state["site_name"]

    def usesSelenium(self):
        return self.uses_selenium
