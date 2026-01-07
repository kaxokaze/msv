rd /s /q "obfuscated"

mkdir "obfuscated"
mkdir "obfuscated\\svLib"
mkdir "obfuscated\\svLib\\agent"
mkdir "obfuscated\\svLib\\drivers"
mkdir "obfuscated\\svLib\\exceptions"
mkdir "obfuscated\\svLib\\gui"
mkdir "obfuscated\\svLib\\gui\\components"
mkdir "obfuscated\\svLib\\gui\\helpers"
mkdir "obfuscated\\svLib\\log"
mkdir "obfuscated\\svLib\\scraper"
mkdir "obfuscated\\svLib\\system"
mkdir "obfuscated\\svLib\\userData"
mkdir "obfuscated\\svLib\\utils"
mkdir "obfuscated\\svLib\\viewModel"
mkdir "obfuscated\\svLib\\viewModel\\helpers"

robocopy "..\\selenium" "obfuscated\\selenium" /MIR
robocopy "..\\dicttoxml" "obfuscated\\dicttoxml" /MIR
robocopy "..\\bin" "obfuscated\\bin" /MIR


copy /y "..\\svLib\\globalConstants.py" "obfuscated\\svLib\\"
copy /y "..\\svLib\\drivers\\undetectedDriver.py" "obfuscated\\svLib\\drivers\\"

pyminifier --obfuscate-variables --obfuscate-builtins --obfuscate-functions --replacement-length=15  ..\siteVisitor.pyw >> obfuscated\siteVisitor.pyw
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\agent\__init__.py >> obfuscated\svLib\agent\__init__.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\agent\agentScheduler.py >> obfuscated\svLib\agent\agentScheduler.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\agent\agentModel.py >> obfuscated\svLib\agent\agentModel.py
pyminifier --obfuscate-builtins --replacement-length=15  ..\svLib\agent\visitWorker.py >> obfuscated\svLib\agent\visitWorker.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\exceptions\chrome_page_exception.py >> obfuscated\svLib\exceptions\chrome_page_exception.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\drivers\driverUpdater.py >> obfuscated\svLib\drivers\driverUpdater.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\gui\aboutWindow.py >> obfuscated\svLib\gui\aboutWindow.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\gui\eventsTab.py >> obfuscated\svLib\gui\eventsTab.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\gui\mainTab.py >> obfuscated\svLib\gui\mainTab.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\gui\mainWindow.py >> obfuscated\svLib\gui\mainWindow.py
pyminifier --obfuscate-builtins --replacement-length=15  ..\svLib\gui\optionsTab.py >> obfuscated\svLib\gui\optionsTab.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\gui\scrapProxiesTab.py >> obfuscated\svLib\gui\scrapProxiesTab.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\gui\settingsSaveUi.py >> obfuscated\svLib\gui\settingsSaveUi.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\gui\userScriptsTab.py >> obfuscated\svLib\gui\userScriptsTab.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\gui\components\toolTip.py >> obfuscated\svLib\gui\components\toolTip.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\gui\helpers\__init__.py >> obfuscated\svLib\gui\helpers\__init__.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\log\svLogger.py >> obfuscated\svLib\log\svLogger.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\scraper\__init__.py >> obfuscated\svLib\scraper\__init__.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\scraper\freeProxyListComParser.py >> obfuscated\svLib\scraper\freeProxyListComParser.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\scraper\proxyListPlusComParser.py >> obfuscated\svLib\scraper\proxyListPlusComParser.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\scraper\proxyNovaComParser.py >> obfuscated\svLib\scraper\proxyNovaComParser.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\scraper\proxyScrapeComParser.py >> obfuscated\svLib\scraper\proxyScrapeComParser.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\scraper\proxyScraper.py >> obfuscated\svLib\scraper\proxyScraper.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\scraper\pubProxyComParser.py >> obfuscated\svLib\scraper\pubProxyComParser.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\scraper\scraperModel.py >> obfuscated\svLib\scraper\scraperModel.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\scraper\siteParser.py >> obfuscated\svLib\scraper\siteParser.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\scraper\textRawProxyListParser.py >> obfuscated\svLib\scraper\textRawProxyListParser.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\system\childProcessesManager.py >> obfuscated\svLib\system\childProcessesManager.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\system\psutilReplacer.py >> obfuscated\svLib\system\psutilReplacer.py
pyminifier --obfuscate-builtins --replacement-length=15  ..\svLib\userData\svSettings.py >> obfuscated\svLib\userData\svSettings.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\userData\svSettingsSerializer.py >> obfuscated\svLib\userData\svSettingsSerializer.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\utils\chromeProxyAuth.py >> obfuscated\svLib\utils\chromeProxyAuth.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\utils\guiMouseEvents.py >> obfuscated\svLib\utils\guiMouseEvents.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\utils\seleniumHelpers.py >> obfuscated\svLib\utils\seleniumHelpers.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\utils\stdHelper.py >> obfuscated\svLib\utils\stdHelper.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\viewModel\helpers\__init__.py >> obfuscated\svLib\viewModel\helpers\__init__.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\viewModel\eventsTabViewModel.py >> obfuscated\svLib\viewModel\eventsTabViewModel.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\viewModel\mainTabViewModel.py >> obfuscated\svLib\viewModel\mainTabViewModel.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\viewModel\mainWindowViewModel.py >> obfuscated\svLib\viewModel\mainWindowViewModel.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\viewModel\optionsTabViewModel.py >> obfuscated\svLib\viewModel\optionsTabViewModel.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\viewModel\scrapProxiesTabViewModel.py >> obfuscated\svLib\viewModel\scrapProxiesTabViewModel.py
pyminifier --obfuscate-builtins --replacement-length=15  ..\svLib\viewModel\settingsViewModel.py >> obfuscated\svLib\viewModel\settingsViewModel.py
pyminifier --obfuscate-variables --replacement-length=15  ..\svLib\viewModel\userScriptsTabViewModel.py >> obfuscated\svLib\viewModel\userScriptsTabViewModel.py
pyminifier --obfuscate-import-methods --replacement-length=15  ..\svLib\utils\threadPool.py >> obfuscated\svLib\utils\threadPool.py