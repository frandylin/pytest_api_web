from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://www.acy-zh.cloud/open-live-account")
wait = WebDriverWait(browser, 10)
actions = ActionChains(browser)

#language test-------------
language_dropdown = browser.find_element(By.CLASS_NAME, 'style__StyledDropdownWrap-sc-itq4ug-14.dZYvIy')
language_dropdown.click()
language_chinese = browser.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div[2]/div/div/div/div/ul/li[3]')
#perform mouse operations using ActionChains
actions.move_to_element(language_dropdown).click(language_chinese).perform()
time.sleep(3)

#country test-----------
country_container = browser.find_element(By.CLASS_NAME, 'select.css-b62m3t-container')
country_container.click()
country_listbox = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1rhcplz-menu')))
hongkong_option = country_listbox.find_element(By.CSS_SELECTOR, 'div[id="react-select-2-option-5"]')
hongkong_option.click()
hongkong_flag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'flag.hk')))
time.sleep(2)
country_container.click()
country_listbox = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1rhcplz-menu')))
taiwan_option = country_listbox.find_element(By.CSS_SELECTOR, 'div[id="react-select-2-option-7"]')
taiwan_option.click()
time.sleep(2)

#name test-----------
first_name = browser.find_element(By.NAME, 'firstName')
last_name = browser.find_element(By.NAME, 'lastName')
first_name.send_keys('Frandy')
last_name.send_keys('Lin')

#phone number test ----------
flag_dropdown = browser.find_element(By.CLASS_NAME, 'flag-dropdown')
flag_dropdown.click()
flag_listbox = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'country-list.dropdown')))
search_box = browser.find_element(By.CLASS_NAME, 'search-box.search-class-box')
search_box.send_keys('+41')
switzerland_option = browser.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div[2]/div/form/div/div/div[2]/div/div[3]/div/div[1]/div/div[2]/ul/li[3]')
switzerland_option.click()
time.sleep(2)
flag_dropdown.click()
flag_listbox = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'country-list.dropdown')))
search_box = browser.find_element(By.CLASS_NAME, 'search-box.search-class-box')
search_box.send_keys('+886')
Taiwan_option = browser.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div[2]/div/form/div/div/div[2]/div/div[3]/div/div[1]/div/div[2]/ul/li[2]')
Taiwan_option.click()
phone_number = browser.find_element(By.CLASS_NAME, 'form-control.phone-input')
phone_number.send_keys('909317920')

#email test----------
email_address = browser.find_element(By.NAME, 'email')
email_address.send_keys('frandyfancy@gmail.com')

#password test----------
create_password = browser.find_element(By.NAME, 'password') 
create_password.send_keys('K25i04r682a')
#prsent password
password_button = browser.find_element(By.CSS_SELECTOR, '[aria-label="Password Icon"]') 
password_button.click()
time.sleep(1)

#chat room test----------
chat_button = browser.find_element(By.XPATH, '/html/body/div/div/div')
chat_button.click()
time.sleep(2)
# hide_chat_button = browser.find_element(By.CLASS_NAME, '/html/body/div/div/div/button')
# hide_chat_button.click()

#continue test----------
continue_button = browser.find_element(By.CLASS_NAME, 'sc-dkrFOg.eQVywz.MuiButtonBase-root.MuiButton-root.MuiButton-text.MuiButton-textPrimary.MuiButton-sizeMedium.MuiButton-textSizeMedium.sc-hLBbgP.jnhPst.MuiButton-root.MuiButton-text.MuiButton-textPrimary.MuiButton-sizeMedium.MuiButton-textSizeMedium.customButton')
continue_button.click()

time.sleep(5)