MSV_VERSION = '2.4.1'
TXT_SEARCH_BY_TEXT = 'TEXTVALUE'
TXT_NOPROXY = 'NOPROXY'
TXT_CONTAINS = 'Contains'
TXT_EQUALS = 'Equals'

BR_PJS = 'PhantomJS'
BR_FX = 'Firefox'
BR_CHR = 'Chrome'

NO_IFRAME = 'NO'

TXT_PRX_START_BTN_ENABLED = 'Scrap'
TXT_PRX_START_BTN_GATHERING = 'Gathering...'
TXT_PRX_START_BTN_STOPPING = 'Stopping...'

PROGRAM_TITLE = "Mass Site Visitor"
ABOUT_TITLE = "About"

EVENTS_TAB_NAME = "Events"
EVENTS_TAB_STATS = "Stats"
EVENTS_TAB_VIS_STATUS = "Visits Status"
EVENTS_TAB_COMPL_VISITS = "Completed Visits"
EVENTS_TAB_TIMEOUTS = "Timed out Requests"
EVENTS_TAB_W_THREADS = "Worker Threads"
EVENTS_TAB_SCH_VISITS = "Scheduled Visits"
EVENTS_TAB_ERRS = "Errors"
EVENTS_TAB_SUCC_VISITS = "Successful Visits"
EVENTS_TAB_ALL_THREADS = "All threads"
EVENTS_TAB_LOG = "Log"

USCRIPTS_TAB_NAME = "User Scripts (Autoclicker)"
USCRIPTS_NEW_SCRIPT = "Add new site script"
USCRIPTS_NEW_SCRIPT_WARN = "WARNING: When a custom user script for the URL exists - it will be executed before " \
                           "auto-random clicks and/or scrolls you've set up. It will be executed once, then the auto-" \
                           "random\nbehavior (click, then scroll, if set up), and then the visit is done"
USCRIPTS_USER_SCRIPTS = "User Scripts (custom behaviour for site URLs)"
USCRIPTS_AUTO_BEHAVIOR = "Auto-Random Behavior (user simulation)"
USCRIPTS_RANDOM_CLICK = "Random Click"
USCRIPTS_RANDOM_SCROLL = "Random Scroll"
USCRIPTS_ENABLE_CLICKS = "Enable clicking"
USCRIPTS_CLICK_LINKS_LABEL = "Click links:"
USCRIPTS_NUM_CLICKS = "Total clicks:"
USCRIPTS_SCROLL = "Scroll "
USCRIPTS_PERCENT_OF_PAGE = "% of the page"
USCRIPTS_SCROLL_AFTER = "After"
USCRIPTS_SCROLL_SECONDS_1 = "seconds"
USCRIPTS_SCROLL_OVER = "Over"
USCRIPTS_SCROLL_SECONDS_2 = "seconds"
USCRIPTS_ENABLE_SCROLL = "Enable scrolling"
USCRIPTS_PERCENT_SCROLL_HINT_1 = "The \"distance\" to scroll the page,as a"
USCRIPTS_PERCENT_SCROLL_HINT_2 = "percentage of the page size (0-100). This scroll"
USCRIPTS_PERCENT_SCROLL_HINT_3 = "will happen for EVERY auto-random click if they"
USCRIPTS_PERCENT_SCROLL_HINT_4 = "are enabled"
USCRIPTS_AFTER_SCROLL_HINT_1 = "Start scrolling the page after the time, randomly"
USCRIPTS_AFTER_SCROLL_HINT_2 = "selected from the specified time range. But the"
USCRIPTS_AFTER_SCROLL_HINT_3 = "'stay on page interval' from 'Options tab' ('Page"
USCRIPTS_AFTER_SCROLL_HINT_4 = "Visit Simulation' section) will also apply"
USCRIPTS_OVER_SCROLL_HINT_1 = "Perform the scroll over the time, randomly"
USCRIPTS_OVER_SCROLL_HINT_2 = "selected from the specified time range"
USCRIPTS_OVER_SCROLL_HINT_3 = "(the longer the time - the slower the scroll)"
USCRIPTS_CLICK_TIME_TIP_1 = "Tip: Options tabs has a 'Page Visit Simulation' section, which specifies time range to\n"
USCRIPTS_CLICK_TIME_TIP_2 = "wait before each consecutive click (for auto-random clicks), or the wait time for script\n"
USCRIPTS_CLICK_TIME_TIP_3 = "execution (before the click) for userscripts. For userscripts time to wait after script\n"
USCRIPTS_CLICK_TIME_TIP_4 = "executes a targeted click can be specified there too."
USCRIPTS_SAVE = "Save"
USCRIPTS_DISCARD = "Discard"
USCRIPTS_RESET_DEFAULT = "Reset to Defaults"
USCRIPTS_IF_URL = "If url"
USCRIPTS_FIND_ELT = "find element"
USCRIPTS_BY_ATTR = "by attribute"
USCRIPTS_WHICH = "which"
USCRIPTS_A_VAL = "a value"
USCRIPTS_IS_IN_FRAME = "is in iframe?"
USCRIPTS_IFRAME_VAL = "iframe val"
USCRIPTS_CLICK_WITH_CHANCE = "and CLICK with chance"
USCRIPTS_PERCENT = "%"

SAVING_SETTING_HINT_1 = "The changes will only take effect (and persist"
SAVING_SETTING_HINT_2 = "to file), when the Save button is clicked"

DISCARDING_SETTING_HINT_1 = "Discard all unsaved settings, set their"
DISCARDING_SETTING_HINT_2 = "displayed values in Options/Userscripts"
DISCARDING_SETTING_HINT_3 = "back to their actual values"

RESETTING_SETTING_HINT_1 = "This will reset settings in UI back to"
RESETTING_SETTING_HINT_2 = "their defaults, but will take effect"
RESETTING_SETTING_HINT_3 = "only if you press the Save button"

AUTO_RANDOM_ANY_LINKS = "All links"
AUTO_RANDOM_INTERNAL_LINKS = "Only internal links (lead to pages within the site)"
AUTO_RANDOM_EXTERNAL_LINKS = "Only external links (lead to the outside websites)"

OPTIONS_TAB_NAME = "Options"
OPTIONS_TAB_SETTINGS = "Settings"
OPTIONS_TAB_VISITOR_BEHAV = "Visitor Behavior"
OPTIONS_TAB_SAVE_SNAPS = "Save page snapshots"
OPTIONS_TAB_OPEN_FOLDER = "Open folder"
OPTIONS_TAB_COUNT_ONLY_SUCC = "Only count successful visits (toward the total visits progress)"
OPTIONS_TAB_BROWSER_RES_LIST = "Browser resolutions list (selected randomly at runtime)"
OPTIONS_TAB_PROXY_HEALTH = "Proxy health"
OPTIONS_TAB_PROXY_TIMEOUT = "Proxy timeout delay, seconds"
OPTIONS_TAB_PROXY_TIMEOUT_HINT = ("Minimal amount of bytes to consider a successful server response\n"
                                  "Note: 39 is the default PhantomJS pagesize form an 'empty' document.\n"
                                  "But a proxy server might return an error message as an html page that is 500-1k "
                                  "bytes long.")
OPTIONS_TAB_MAX_FAILS = ("Maximum amount of fails without successes,\n"
                         "after which proxy is completely disregarded for any future requests")
OPTIONS_TAB_JS_REF_INJ = "JavaScript Referrer Injection"
OPTIONS_TAB_ENABLE_JS_REF_INJ = "Enable javascript referrer injection (for Google Analytics, Bounce Rate)"
OPTIONS_TAB_JS_REF_INJ_HINT_1 = "With Firefox you better set the 'minimal correct response size' option"
OPTIONS_TAB_JS_REF_INJ_HINT_2 = "to something relatively low (i.e.1100), because after injection Firefox"
OPTIONS_TAB_JS_REF_INJ_HINT_3 = "returns prematurely and doesn't wait for the page to fully load, therefore you'd"
OPTIONS_TAB_JS_REF_INJ_HINT_4 = "also have to set 'stay on page interval' to something high, to wait manually,"
OPTIONS_TAB_JS_REF_INJ_HINT_5 = "and use Firefox with injection ONLY for Alexa analytics."
OPTIONS_TAB_JS_REF_INJ_TIMEOUT = "JS injection timeout delay, seconds"
OPTIONS_TAB_JS_ADDITIONAL_CAPABILITIES = "Additional services/plugins/capabilities"
OPTIONS_TAB_ENABLE_ALEXA = "Enable Alexa toolbar (for Alexa analytics, works with Chrome[non-headless] "\
                           "and Firefox drivers only)"
OPTIONS_TAB_ENABLE_SIMILARWEB = "Enable Similarweb browser extension (for Alexa analytics, works with Chrome"\
                                 "[non-headless] and Firefox drivers only)"
OPTIONS_TAB_ENABLE_IMAGES = "Load Images"
OPTIONS_TAB_VISIT_SIMULATION = "Page Visit Simulation"
OPTIONS_TAB_MIN_STAY_ON_PAGE_INT = "Minimal stay on page interval (before each click for auto-random clicks), seconds"
OPTIONS_TAB_MAX_STAY_ON_PAGE_INT = "Maximum stay on page interval (before each click for auto-random clicks), seconds"
OPTIONS_TAB_AFTER_SCRIPT_INT = "Wait after the user script execution (only if executed), seconds"
OPTIONS_TAB_LOCALE_LIST = "Locale list"
OPTIONS_TAB_SPOOF_LOCALES = "Spoof locales"
OPTIONS_TAB_COOKIES = "Cookies"
OPTIONS_TAB_ENABLE_COOKIES = "Enable cookies - file as json aray of cookie objects (see the default cookies.json for detailed format)"
OPTIONS_TAB_COOKIES_FILE = "Cookies list file:"
OPTIONS_TAB_COOKIES_FILE_BUTTON = "Browse"
OPTIONS_TAB_SAVE = "Save"

MAIN_TAB_CHCK_ON = "On"
MAIN_TAB_CHCK_OFF = "Off"
MAIN_TAB_TAB_NAME = "Visitor"
MAIN_TAB_TARG_OPTIONS = "Target Options"
MAIN_TAB_WEBSITES_TXT = "Website(s),\nOne per line"
MAIN_TAB_VISITS = "Visits"
MAIN_TAB_THREADS = "Threads"
MAIN_TAB_THREADS_HINT_1 = "The amount of browser sessions"
MAIN_TAB_THREADS_HINT_2 = "to run in parallel."
MAIN_TAB_BROWSER = "Browser:"
MAIN_TAB_BROWSER_HINT_1 = "You MUST have it installed on your PC first"
MAIN_TAB_BROWSER_HINT_2 = "unless you are using PhantomJS"
MAIN_TAB_FF_NIGHTLY_HINT_2 = "Nightly or Developer Edition preferred"
MAIN_TAB_UPD_DRIVERS = "Update browser drivers"
MAIN_TAB_UPD_DRIVERS_HINT_1 = "If you see errors, when launching chrome/firefox, saying"
MAIN_TAB_UPD_DRIVERS_HINT_2 = "things like \"your browser version doesn't correspond"
MAIN_TAB_UPD_DRIVERS_HINT_3 = "to the driver version\" - use this button to fix that."
MAIN_TAB_HEADLESS = "Headless mode"
MAIN_TAB_HEADLESS_HINT_1 = "Warning! Will create multiple"
MAIN_TAB_HEADLESS_HINT_2 = "browser windows for"
MAIN_TAB_HEADLESS_HINT_3 = "non-headless browsers"
MAIN_TAB_HIDE_OFF_SCREEN = "Hide off-screen"
MAIN_TAB_HIDE_OFF_SCREEN_HINT_1 = "For windowed (non-headless) mode. Might not be immediate"
MAIN_TAB_HIDE_OFF_SCREEN_HINT_2 = "with Firefox, however it is usually created without"
MAIN_TAB_HIDE_OFF_SCREEN_HINT_3 = "taking focus, while Chrome is."
MAIN_TAB_BROWSER_PATH = "Browser path:"
MAIN_TAB_BROWSER_PATH_HINT = "Optional. You can leave empty"
MAIN_TAB_BROWSER_PATH_EF_HINT_1 = "You can leave empty. Only enter the full path to executable"
MAIN_TAB_BROWSER_PATH_EF_HINT_2 = "if you see errors in the log about not being able to find"
MAIN_TAB_BROWSER_PATH_EF_HINT_3 = "the browser executable"
MAIN_TAB_REQ_OPTIONS = "Request Options"
MAIN_TAB_LOAD_REF_LIST = "Load referrer list"
MAIN_TAB_CLEAR_REF_LIST = "Clear referrer list"
MAIN_TAB_LOAD_AGENT_LIST = "Load user agent list"
MAIN_TAB_CLEAR_AGENT_LIST = "Clear user agent list"
MAIN_TAB_LOAD_PROXY_LIST = "Load proxy list"
MAIN_TAB_CLEAR_PROXY_LIST = "Clear proxy list"
MAIN_TAB_LOAD_PROXY_HINT_1 = "The loaded proxies are added to the existing ones"
MAIN_TAB_LOAD_PROXY_HINT_2 = "with duplicate checking: if the proxy is in the list"
MAIN_TAB_LOAD_PROXY_HINT_3 = "already, it won't be added"
MAIN_TAB_TEST_PROXIES = "Test Proxies"
MAIN_TAB_TEST_PROXIES_HINT_1 = "Will use the Proxy Health settings (in Options window),"
MAIN_TAB_TEST_PROXIES_HINT_2 = "like max timeout on the proxy and number of attempts,"
MAIN_TAB_TEST_PROXIES_HINT_3 = "and thread count as set at the top of the main window"
MAIN_TAB_REFERERS = "Referrers:"
MAIN_TAB_UAS = "User Agents:"
MAIN_TAB_PROXIES = "Proxies:"
MAIN_TAB_VISITS_PROGRESS = "Visits Progress"
MAIN_TAB_START = "START"
MAIN_TAB_STOP = "STOP"
MAIN_TAB_VISITS_2 = "Visits:"
MAIN_TAB_THREADS_2 = "Threads:"

SCRAP_TAB_NAME = "Scrap proxies"
SCRAP_TAB_SELECT_SITE = "Select a site-proxy directory:"
SCRAP_TAB_PROXY_TRANSPARENT = "Transparent"
SCRAP_TAB_PROXY_ANON = "Anonymous"
SCRAP_TAB_PROXY_ELITE = "Elite (High Anonymity)"
SCRAP_TAB_SAVE_TO = "Save to:"
SCRAP_TAB_CHOOSE = "Choose"
SCRAP_TAB_LOAD_LIST_INSTANTLY = "Load into the list right away"
SCRAP_TAB_LOAD_LIST_INSTANTLY_HINT_1 = "The imported proxies are added to the existing ones"
SCRAP_TAB_LOAD_LIST_INSTANTLY_HINT_2 = "with duplicate checking: if the proxy is in the list"
SCRAP_TAB_LOAD_LIST_INSTANTLY_HINT_3 = "already, it won't be added."
SCRAP_TAB_LOAD_LIST_INSTANTLY_HINT_4 = "Pro-tip: don't change the target file while scraping for"
SCRAP_TAB_LOAD_LIST_INSTANTLY_HINT_5 = "this to work."
SCRAP_TAB_DESELECT_ALL_COUNTRIES = "Deselect All Countries"
SCRAP_TAB_SELECT_ALL_COUNTRIES = "Select All Countries"
SCRAP_TAB_SELECT_COUNTRIES = "Select Countries"
SCRAP_TAB_STOP = "Stop"

MENU_FILE = 'File'
MENU_ITEM_EXP_HEALTHY_PROXIES = 'Export Healthy (green) Proxies'
MENU_ITEM_EXP_NON_LAGGING_PROXIES = 'Export Non-Lagging (All non-orange) Proxies'
MENU_ITEM_SAVE_LOG = 'Save events to a log file'

MENU_HELP = 'Help'
MENU_ITEM_ABOUT = 'About'

ABOUT_TEXT_0 = "Mass Site Visitor v%s" % MSV_VERSION
ABOUT_TEXT_1 = \
    """\tMass Site Visitor (MSV) is designed to generate large amounts of traffic to websites of your choice through the list of proxies in a 
multi-threaded way. You can set referrers and user agents, which along with proxies will be randomly selected to create a browser session.
You can also select to save an image snapshot for every visit (to see how web-site is seen from different IPs). User behavior can be simulated
int the browser while it's on page - clicks and scrolling can be done by the bot (check out User Scripts/ Autoclicker tab). You can filter out
non-responsive proxies from the ones that work, and save them to a file (Settings - Export Healthy Proxies after running live sessions or test).\n
        Referrers, user agents and proxies should be stored in a text-file, one per line, and can be appended to an already loaded list in the 
program by pressing the 'Load the <something> list' button.\n
        If you don't have a proxy list of your own, and the one supplied with MSV isn't satisfactory (with time those proxies might cease to work),
there is an ability to scrap public proxies from the web, Scrap Proxies tab. Remember to add the word socks5 after the ip of a public socks4/5 proxy,
separated by a single space, but if you are scraping these proxies from the web, you don't have to worry about that, MSV will handle this.\n
        Don't forget to update browser drivers - needed for MSV to work with Chrome and Firefox - there's a button for this on the Visitor tab.\n
        There is a pdf file with all the tips and instructions about the usage of MSV available. See it, if you have some questions."""
ABOUT_TEXT_2 = "By headshote@gmail.com, 2016"

ABOUT_TEXT_THIRD_PARTY = "Third party download and info links:"
third_party_downloads = {
    "Geckodriver (firefox)": "https://github.com/mozilla/geckodriver/releases",
    "Chromedriver": "https://sites.google.com/chromium.org/driver/",
    "PhantomJS (headless browser)": "http://phantomjs.org/download.html",
    "Popular User Agents": "https://techblog.willshouse.com/2012/01/03/most-common-user-agents/",
    "Locales for different languages": "https://www.metamodpro.com/browser-language-codes",
    "Private Proxies by Luminati (BrightData)": "https://brightdata.grsm.io/msv",
    "Private Proxies by Infatica": "https://dashboard.infatica.io/aff.php?aff=68",
}

CHROMEDRIVER_PATH = "bin/chromedriver.exe"

COUNTRY_CODES = {
    "AF": "Afghanistan",
    "AX": "Åland Islands",
    "AL": "Albania",
    "DZ": "Algeria",
    "AS": "American Samoa",
    "AD": "Andorra",
    "AO": "Angola",
    "AI": "Anguilla",
    "AQ": "Antarctica",
    "AG": "Antigua and Barbuda",
    "AR": "Argentina",
    "AM": "Armenia",
    "AW": "Aruba",
    "AU": "Australia",
    "AT": "Austria",
    "AZ": "Azerbaijan",
    "BS": "Bahamas",
    "BH": "Bahrain",
    "BD": "Bangladesh",
    "BB": "Barbados",
    "BY": "Belarus",
    "BE": "Belgium",
    "BZ": "Belize",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BT": "Bhutan",
    "BO": "Bolivia (Plurinational State of)",
    "BQ": "Bonaire, Sint Eustatius and Saba",
    "BA": "Bosnia and Herzegovina",
    "BW": "Botswana",
    "BV": "Bouvet Island",
    "BR": "Brazil",
    "IO": "British Indian Ocean Territory",
    "BN": "Brunei Darussalam",
    "BG": "Bulgaria",
    "BF": "Burkina Faso",
    "BI": "Burundi",
    "CV": "Cabo Verde",
    "KH": "Cambodia",
    "CM": "Cameroon",
    "CA": "Canada",
    "KY": "Cayman Islands",
    "CF": "Central African Republic",
    "TD": "Chad",
    "CL": "Chile",
    "CN": "China",
    "CX": "Christmas Island",
    "CC": "Cocos (Keeling) Islands",
    "CO": "Colombia",
    "KM": "Comoros",
    "CG": "Congo",
    "CD": "Congo, Democratic Republic of the",
    "CK": "Cook Islands",
    "CR": "Costa Rica",
    "CI": "Côte d'Ivoire",
    "HR": "Croatia",
    "CU": "Cuba",
    "CW": "Curaçao",
    "CY": "Cyprus",
    "CZ": "Czechia",
    "DK": "Denmark",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "EC": "Ecuador",
    "EG": "Egypt",
    "SV": "El Salvador",
    "GQ": "Equatorial Guinea",
    "ER": "Eritrea",
    "EE": "Estonia",
    "SZ": "Eswatini",
    "ET": "Ethiopia",
    "FK": "Falkland Islands (Malvinas)",
    "FO": "Faroe Islands",
    "FJ": "Fiji",
    "FI": "Finland",
    "FR": "France",
    "GF": "French Guiana",
    "PF": "French Polynesia",
    "TF": "French Southern Territories",
    "GA": "Gabon",
    "GM": "Gambia",
    "GE": "Georgia",
    "DE": "Germany",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GR": "Greece",
    "GL": "Greenland",
    "GD": "Grenada",
    "GP": "Guadeloupe",
    "GU": "Guam",
    "GT": "Guatemala",
    "GG": "Guernsey",
    "GN": "Guinea",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HT": "Haiti",
    "HM": "Heard Island and McDonald Islands",
    "VA": "Holy See",
    "HN": "Honduras",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IS": "Iceland",
    "IN": "India",
    "ID": "Indonesia",
    "IR": "Iran (Islamic Republic of)",
    "IQ": "Iraq",
    "IE": "Ireland",
    "IM": "Isle of Man",
    "IL": "Israel",
    "IT": "Italy",
    "JM": "Jamaica",
    "JP": "Japan",
    "JE": "Jersey",
    "JO": "Jordan",
    "KZ": "Kazakhstan",
    "KE": "Kenya",
    "KI": "Kiribati",
    "KP": "Korea (Democratic People's Republic of)",
    "KR": "Korea, Republic of",
    "KW": "Kuwait",
    "KG": "Kyrgyzstan",
    "LA": "Lao People's Democratic Republic",
    "LV": "Latvia",
    "LB": "Lebanon",
    "LS": "Lesotho",
    "LR": "Liberia",
    "LY": "Libya",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MO": "Macao",
    "MG": "Madagascar",
    "MW": "Malawi",
    "MY": "Malaysia",
    "MV": "Maldives",
    "ML": "Mali",
    "MT": "Malta",
    "MH": "Marshall Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MU": "Mauritius",
    "YT": "Mayotte",
    "MX": "Mexico",
    "FM": "Micronesia (Federated States of)",
    "MD": "Moldova, Republic of",
    "MC": "Monaco",
    "MN": "Mongolia",
    "ME": "Montenegro",
    "MS": "Montserrat",
    "MA": "Morocco",
    "MZ": "Mozambique",
    "MM": "Myanmar",
    "NA": "Namibia",
    "NR": "Nauru",
    "NP": "Nepal",
    "NL": "Netherlands",
    "NC": "New Caledonia",
    "NZ": "New Zealand",
    "NI": "Nicaragua",
    "NE": "Niger",
    "NG": "Nigeria",
    "NU": "Niue",
    "NF": "Norfolk Island",
    "MK": "North Macedonia",
    "MP": "Northern Mariana Islands",
    "NO": "Norway",
    "OM": "Oman",
    "PK": "Pakistan",
    "PW": "Palau",
    "PS": "Palestine, State of",
    "PA": "Panama",
    "PG": "Papua New Guinea",
    "PY": "Paraguay",
    "PE": "Peru",
    "PH": "Philippines",
    "PN": "Pitcairn",
    "PL": "Poland",
    "PT": "Portugal",
    "PR": "Puerto Rico",
    "QA": "Qatar",
    "RE": "Réunion",
    "RO": "Romania",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "BL": "Saint Barthélemy",
    "SH": "Saint Helena, Ascension and Tristan da Cunha",
    "KN": "Saint Kitts and Nevis",
    "LC": "Saint Lucia",
    "MF": "Saint Martin (French part)",
    "PM": "Saint Pierre and Miquelon",
    "VC": "Saint Vincent and the Grenadines",
    "WS": "Samoa",
    "SM": "San Marino",
    "ST": "Sao Tome and Principe",
    "SA": "Saudi Arabia",
    "SN": "Senegal",
    "RS": "Serbia",
    "SC": "Seychelles",
    "SL": "Sierra Leone",
    "SG": "Singapore",
    "SX": "Sint Maarten (Dutch part)",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "SB": "Solomon Islands",
    "SO": "Somalia",
    "ZA": "South Africa",
    "GS": "South Georgia and the South Sandwich Islands",
    "SS": "South Sudan",
    "ES": "Spain",
    "LK": "Sri Lanka",
    "SD": "Sudan",
    "SR": "Suriname",
    "SJ": "Svalbard and Jan Mayen",
    "SE": "Sweden",
    "CH": "Switzerland",
    "SY": "Syrian Arab Republic",
    "TW": "Taiwan, Province of China",
    "TJ": "Tajikistan",
    "TZ": "Tanzania, United Republic of",
    "TH": "Thailand",
    "TL": "Timor-Leste",
    "TG": "Togo",
    "TK": "Tokelau",
    "TO": "Tonga",
    "TT": "Trinidad and Tobago",
    "TN": "Tunisia",
    "TR": "Turkey",
    "TM": "Turkmenistan",
    "TC": "Turks and Caicos Islands",
    "TV": "Tuvalu",
    "UG": "Uganda",
    "UA": "Ukraine",
    "AE": "United Arab Emirates",
    "GB": "United Kingdom of Great Britain and Northern Ireland",
    "UM": "United States Minor Outlying Islands",
    "US": "United States of America",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VU": "Vanuatu",
    "VE": "Venezuela (Bolivarian Republic of)",
    "VN": "Viet Nam",
    "VG": "Virgin Islands (British)",
    "VI": "Virgin Islands (U.S.)",
    "WF": "Wallis and Futuna",
    "EH": "Western Sahara",
    "YE": "Yemen",
    "ZM": "Zambia",
    "ZW": "Zimbabwe"
}

ALL_COUNTRIES = "ALL"
