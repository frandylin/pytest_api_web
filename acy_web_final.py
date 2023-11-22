from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pytest
import unittest


class TestWebPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the webdriver once for the entire class
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("https://www.acy-cn.cloud/open-live-account")

    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests in the class are completed
        cls.driver.quit()

    def test01_language_selection(self):
        language_dropdown = self.driver.find_element(By.CLASS_NAME, 'style__StyledDropdownWrap-sc-itq4ug-14.dZYvIy')
        language_dropdown.click()
        language_chinese = self.driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div[2]/div/div/div/div/ul/li[3]')
        language_chinese.click()
        time.sleep(3)

    def test02_country_selection(self):
        country_container = self.driver.find_element(By.CLASS_NAME, 'select.css-b62m3t-container')
        country_container.click()
        country_listbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'css-1rhcplz-menu'))
        )
        hongkong_option = country_listbox.find_element(By.CSS_SELECTOR, 'div[id="react-select-2-option-5"]')
        hongkong_option.click()
        hongkong_flag = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'flag.hk'))
        )
        time.sleep(2)
        country_container.click()
        country_listbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'css-1rhcplz-menu'))
        )
        taiwan_option = country_listbox.find_element(By.CSS_SELECTOR, 'div[id="react-select-2-option-7"]')
        taiwan_option.click()
        time.sleep(2)

    def test03_enter_name(self):
        first_name = self.driver.find_element(By.NAME, 'firstName')
        last_name = self.driver.find_element(By.NAME, 'lastName')
        first_name.send_keys('Frandy')
        last_name.send_keys('Lin')

    def test04_phone_number(self):
        flag_dropdown = self.driver.find_element(By.CLASS_NAME, 'flag-dropdown')
        flag_dropdown.click()
        flag_listbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'country-list.dropdown'))
        )
        search_box = self.driver.find_element(By.CLASS_NAME, 'search-box.search-class-box')
        search_box.send_keys('+41')
        switzerland_option = self.driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div[2]/div/form/div/div/div[2]/div/div[3]/div/div[1]/div/div[2]/ul/li[3]')
        switzerland_option.click()
        time.sleep(2)
        flag_dropdown.click()
        flag_listbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'country-list.dropdown'))
        )
        search_box = self.driver.find_element(By.CLASS_NAME, 'search-box.search-class-box')
        search_box.send_keys('+886')
        Taiwan_option = self.driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div[2]/div/form/div/div/div[2]/div/div[3]/div/div[1]/div/div[2]/ul/li[2]')
        Taiwan_option.click()
        phone_number = self.driver.find_element(By.CLASS_NAME, 'form-control.phone-input')
        phone_number.send_keys('909317920')

    def test05_email_enter(self):
        email_address = self.driver.find_element(By.NAME, 'email')
        email_address.send_keys('frandyfancy@gmail.com')
        
    def test06_password_enter(self):
        create_password = self.driver.find_element(By.NAME, 'password') 
        create_password.send_keys('K25i04r682a')
        
    def test07_present_password(self):
        password_button = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Password Icon"]') 
        password_button.click()
        time.sleep(1)

    def test08_chat_room(self):
        chat_button = self.driver.find_element(By.XPATH, '/html/body/div/div/div')
        chat_button.click()

    def test09_continue_button(self):
        continue_button = self.driver.find_element(By.CLASS_NAME, 'sc-dkrFOg.eQVywz.MuiButtonBase-root.MuiButton-root.MuiButton-text.MuiButton-textPrimary.MuiButton-sizeMedium.MuiButton-textSizeMedium.sc-hLBbgP.jnhPst.MuiButton-root.MuiButton-text.MuiButton-textPrimary.MuiButton-sizeMedium.MuiButton-textSizeMedium.customButton')
        continue_button.click()
        time.sleep(3)

if __name__ == '__main__':
    unittest.main()
