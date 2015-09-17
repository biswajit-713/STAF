__author__ = 'biswajit'

# import the modules
from selenium import webdriver
import os
import sys
from time import sleep

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "STAF_Libs")))
import LibDriver

driver = LibDriver.initialize_driver()
driver.get("http://cleartrip.com")

#sleep(10)
#driver.quit()




