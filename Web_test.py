from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
# from BeautifulReport import BeautifulReport
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://im-stg-web.imdevs.net/#/home")
time.sleep(5)
# appstore = browser.find_element(By.XPATH, '//img[@alt="appstore_url"]')
# appstore.click()
# time.sleep(10)

