# general modules
import traceback
import nose
import unittest
import sys

#selenium modules
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common import exceptions as EX
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.alert import Alert

class IR_Reservation_Inquiry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://www.indianrail.gov.in/between_Imp_Stations.html")
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.driver.execute_script("document.body.style.transform='scale(1)'")

    def test_01_verify_search_params(self):
        driver = self.driver

        try:
            search_sync = WebDriverWait(driver,10).until(lambda driver : driver.find_element(By.CSS_SELECTOR,'td.inside_heading_text').is_displayed())
            assert search_sync == True

            #verify source station tag and that it contains some stations
            elm_source_station = driver.find_element(By.CSS_SELECTOR,"select[name='lccp_src_stncode']")
            assert elm_source_station.is_enabled() == True
            source_options = elm_source_station.find_elements_by_tag_name("option")
            assert len(source_options) > 0

            #verify the calendar image next to the month field
            elm_calendar = driver.find_element_by_xpath("//input[@name='lccp_month' and @alt='Month']/following-sibling::img")
            assert str(elm_calendar.get_attribute("src")).startswith("http") == True

        except NoSuchElementException:
            # print the line number where the error occurs
            print self._testMethodName + " - Error at line number : " + str(sys.exc_traceback.tb_lineno)

        except:
            print traceback.format_exc()

    def test_02_search_train(self):
        driver = self.driver

        try:
            #select the source station
            elm_source_text = driver.find_element_by_css_selector("select[name='lccp_src_stncode'] > option[selected='Selected'] ").text
            elm_source_select = Select(driver.find_element_by_css_selector("select[name='lccp_src_stncode']"))
            elm_source_select.select_by_visible_text(str(elm_source_text))

            #select destination station
            elm_dest_text = driver.find_element_by_xpath("//select[@name='lccp_dstn_stncode']/option[@selected='selected']").get_attribute("value")
            elm_dest_select = Select(driver.find_element_by_name("lccp_dstn_stncode"))
            elm_dest_select.select_by_value(str(elm_dest_text))

            # enter the date of journey and select the journey type
            elm_journey_date = driver.find_elements_by_name("lccp_day")[0]
            elm_journey_month = driver.find_element_by_css_selector("input[name='lccp_month'][alt='Month']")
            elm_journey_date.clear()
            elm_journey_date.send_keys("10")
            elm_journey_month.clear()
            elm_journey_month.send_keys("10")

            elm_journey_type = driver.find_elements_by_xpath("//input[@name='monitor' and @type='radio']")[0]
            elm_journey_type.click()

            #click details
            elm_getdetails_button = driver.find_element_by_css_selector(".btn_style[value='Get Details']")
            elm_getdetails_button.click()

            # wait until the next page loads
            elm_result_table = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,'heading_table_top')))

            # verify the query returned more than 1 result
            elm_train_no = driver.find_elements_by_css_selector("input[name='lccp_trndtl'][type='RADIO']")
            self.assertGreater(len(elm_train_no),1)


        except NoSuchElementException:
            print self._testMethodName + " - Error at line number : " + str(sys.exc_traceback.tb_lineno)
            print sys.exc_info()
        except AttributeError:
            print self._testMethodName + " - Error at line number : " + str(sys.exc_traceback.tb_lineno)
            print sys.exc_info()

    def test_03_verify_tooltip(self):
        driver = self.driver

        # tooltips are generally associated with alt or title attribute
        try:
            elm_origin_radio = driver.find_element_by_css_selector("input[name='lccp_trndtl'][type='RADIO']")
            elm_table_body = elm_origin_radio.find_element_by_xpath("../../..")
            elm_result_list = elm_table_body.find_elements_by_xpath("tr")
            count = len(elm_result_list)
            for i in range(2,count):
                elm_origin_cell = elm_result_list[i].find_elements_by_xpath("td")[2]
                #print elm_origin_cell.get_attribute("title")
                action_chain = ActionChains(driver)
                builder = action_chain.move_to_element(to_element=elm_origin_cell)
                sleep(1)
                builder.perform()
                location =  elm_origin_cell.location
                size = elm_origin_cell.size

        except NoSuchElementException:
            print self._testMethodName + " - Error in line number : " + str(sys.exc_traceback.tb_lineno)

    def test_04_get_availability(self):
        driver = self.driver

        elm_get_availability = driver.find_element_by_css_selector(".btn_style[name='lccp_submitacc']")
        elm_get_availability.click()

        if EC.alert_is_present:
            alert = driver.switch_to.alert
            sleep(2)
            alert.accept()
        else:
            raise EC.NoAlertPresentException

        driver.back()
        sleep(5)

    def test_05_context_click(self):

        driver = self.driver

        try:
            elm_catering_charges = driver.find_element_by_link_text("Catering Charges")
            action_chain = ActionChains(driver)

            # open link in a new tab with context click
            builder = action_chain.context_click(on_element=elm_catering_charges)
            sleep(0.5)
            builder.send_keys(Keys.DOWN).send_keys(Keys.RETURN).send_keys(Keys.DOWN).send_keys(Keys.ESCAPE).perform()
            sleep(1)
            window_handles = driver.window_handles
            print driver.current_window_handle
            driver.switch_to.window(window_handles[-1])
            print driver.current_window_handle
            driver.close()
            driver.switch_to.window(window_handles[0])

        except EX.StaleElementReferenceException:
            print self._testMethodName + " - Error at line number : " + sys.exc_traceback.tb_lineno
            print sys.exc_info()
        except NoSuchElementException:
            print self._testMethodName + " - Error at line number : " + sys.exc_traceback.tb_lineno
            print sys.exc_info()
        except EX.NoSuchWindowException:
            print self._testMethodName + " - Error at line number : " + sys.exc_traceback.tb_lineno
            print sys.exc_info()

    def test_06_link_in_new_window(self):

        driver = self.driver

        try:
            elm_catering_charges = driver.find_element_by_link_text("Catering Charges")
            action_chain = ActionChains(driver)

            # open link in a new window
            action_chain.send_keys(Keys.SHIFT).click(elm_catering_charges).send_keys(Keys.SHIFT).perform()
            sleep(2)
            print driver.current_window_handle
            window_handles = driver.window_handles
            driver.switch_to.window(window_handles[-1])
            print driver.current_window_handle
            driver.close()
            driver.switch_to.window(window_handles[0])


        except EX.StaleElementReferenceException:
            print self._testMethodName + " - Error at line number : " + sys.exc_traceback.tb_lineno
            print sys.exc_info()
        except NoSuchElementException:
            print self._testMethodName + " - Error at line number : " + sys.exc_traceback.tb_lineno
            print sys.exc_info()


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


