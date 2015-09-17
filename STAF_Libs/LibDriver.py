__author__ = 'biswajit'

import os
from ConfigParser import SafeConfigParser
from xml.dom import minidom
from pyjavaproperties import Properties
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# define ConfigParser class
class ConfigParser:

    def __init__(self):
        self.config_file = os.path.join(os.getcwd(), '..' + os.sep + 'STAF_Config', 'STAF_Config.ini')

    def get_config(self, section, param):
        parser = SafeConfigParser()
        parser.read(self.config_file)

        return parser.get(section, param)

# Test scenario driver class
class TestScenarioDriver:
    def __init__(self):
        self.test_list_file = os.path.join(os.getcwd(), '..' + os.sep + 'STAF_Config', 'TestCase_Driver.xml')

    def get_test_list(self):
        test_xml = minidom.parse(self.test_list_file)

        test_scenarios = test_xml.getElementsByTagName('Scenario')

        scenario_list = []

        for scenario in test_scenarios:
            if scenario.getAttribute('Value').encode('ascii', 'ignore').upper() == 'YES':
                scenario_list.append(scenario.getAttribute('Name').encode('ascii', 'ignore'))

        return scenario_list


# function to read UI map properties and return the property value
def get_property_value(property_name):

    cur_path = os.getcwd()
    ui_map_file = os.path.join(cur_path, '..' + os.sep, 'STAF_Config' + os.sep + 'ui_map.properties')
    ui_map_file = os.path.abspath(ui_map_file)

    prop = Properties()
    prop.load(open(ui_map_file))

    if prop.getProperty(property_name).strip() == "":
        return "Property not found"
    else:
        return prop.getProperty(property_name)

# function to return the object reference
def get_object(driver, property_name):

    prop_pair = get_property_value(property_name)

    if prop_pair == "Property not found":
        return None

    strPropName = prop_pair.split("=")[0]
    strPropValue = prop_pair.split("=")[1]

    try:
        if strPropName.lower() == "id":
            return driver.find_element_by_id(strPropValue)
        elif strPropName.lower() == "name":
            return driver.find_element_by_name(strPropValue)
        elif strPropName.lower() == "linktext":
            return driver.find_element_by_link_text(strPropValue)
        elif strPropName.lower() == "partialtext":
            return driver.find_element_by_partial_link_text(strPropValue)
        elif strPropName.lower() == "css":
            return driver.find_element_by_css_selector(strPropValue)
        elif strPropName.lower() == "xpath":
            return driver.find_element_by_xpath("xpath")
        else :
            return None
    except NoSuchElementException:
        return None

# function to initialize the web driver details
def initialize_driver():

    config_parser = ConfigParser()

    browser = config_parser.get_config("Host", "Browser")
    version = config_parser.get_config("Host", "Version")
    platform = config_parser.get_config("Host", "Platform")

    if browser.lower() == "firefox":
        dc_firefox = DC.FIREFOX.copy()

        dc_firefox['browserName'] = browser
        dc_firefox['version'] = version
        dc_firefox['platform'] = platform

        ff_profile = webdriver.FirefoxProfile()
        ff_profile.accept_untrusted_certs = True

        is_default_download = config_parser.get_config("Firefox", "browser.download.folderList")
        show_when_starting = config_parser.get_config("Firefox", "browser.download.manager.showWhenStarting")
        download_dir = config_parser.get_config("Firefox", "browser.download.dir")
        ask_save_to_disk = config_parser.get_config("Firefox", "browser.helperApps.neverAsk.saveToDisk")
        ff_exec_path = config_parser.get_config("Firefox", "Executable_Path")

        ff_profile.set_preference("browser.download.folderList", is_default_download)
        ff_profile.set_preference("browser.download.manager.showWhenStarting", show_when_starting)
        ff_profile.set_preference("browser.download.dir", download_dir)
        ff_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ask_save_to_disk)
        ff_profile.set_preference("webdriver.firefox.bin",ff_exec_path)

        #ff_binary_path = config_parser.get_config("Firefox", "Executable_Path")
        #ff_binary = FirefoxBinary(ff_binary_path)
        driver = webdriver.Firefox(firefox_profile=ff_profile)

    elif browser.lower() == "chrome":
        dc_chrome = DC.CHROME.copy()
        chrome_options = webdriver.ChromeOptions()

        dc_chrome['browserName'] = browser
        dc_chrome['version'] = version
        dc_chrome['platform'] = platform

        # chrome launch mode - maximized or regular
        is_max = config_parser.get_config("Chrome","start_maximized")
        if is_max.lower() == "true":
            chrome_options.add_argument("--start-maximized")
        elif is_max.lower() == "false":
            chrome_options.add_argument("--start-minimized")

        # chrome extension
        disable_extension = config_parser.get_config("Chrome","disable_extension")
        if disable_extension.lower() == "true":
            chrome_options.add_argument("--disable-extensions")
        elif disable_extension.lower() == "false":
            extension_path = config_parser.get_config("Chrome","add_extension")
            chrome_options.add_extension(open(extension_path))

        # download directory
        download_dir = config_parser.get_config("Chrome","download.default_directory")
        print download_dir
        chrome_options.add_experimental_option("prefs", {"download.default_directory" : download_dir})

        # load images on browser loading or not
        display_image = config_parser.get_config("Chrome","display_image")
        if display_image.lower() == "yes":
            chrome_options.add_experimental_option("prefs",{"profile.default_content_settings.images" : 1})
        elif display_image.lower() == "no":
            chrome_options.add_experimental_option("prefs",{"profile.default_content_settings.images" : 2})

        dc_chrome.update(chrome_options.to_capabilities())
        driver = webdriver.Chrome(desired_capabilities = dc_chrome)

    elif browser.lower() == "internetexplorer":
        dc_ie = DC.INTERNETEXPLORER.copy()
        ie_exec_path = config_parser.get_config("InternetExplorer","Executable_Path")

        dc_ie['browserName'] = browser
        dc_ie['version'] = version
        dc_ie['platform'] = platform

        dc_ie["ignoreZoomSetting"] = bool(config_parser.get_config("InternetExplorer","ignoreZoomSetting"))
        dc_ie["requireWindowFocus"] = bool(config_parser.get_config("InternetExplorer","requireWindowFocus"))
        dc_ie["ie.ensureCleanSession"] = bool(config_parser.get_config("InternetExplorer","ie.ensureCleanSession"))

        driver = webdriver.Ie(executable_path=ie_exec_path, capabilities = dc_ie)


    driver.maximize_window()

    # zoom the browser to 100% - applicable for IE, chrome and firefox
    if browser.lower() == "interexplorer" or browser.lower() == "chrome":
        driver.execute_script("document.body.style.transform='scale(1)'")

    return driver




