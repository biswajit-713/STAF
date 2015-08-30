__author__ = 'biswajit'

import os
from ConfigParser import SafeConfigParser
from xml.dom import minidom
from pyjavaproperties import Properties


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


