########
# Our very own exception for chrome timeout/unavailable/connection reset errors
########
class ChromePageException(Exception):
    pass
