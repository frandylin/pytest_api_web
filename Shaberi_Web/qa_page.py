from selenium import webdriver
import time
import shutil
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



browser = webdriver.Chrome()
browser.maximize_window()
wait = WebDriverWait(browser, 10)
actions = ActionChains(browser)
current_url = browser.current_url


### 正式開始測試 ### 
browser.get("https://www.shaberi.com/tw")

#qa page test --------------
qa_bt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/ul/li[2]/a')
qa_bt.click()
wait.until(EC.url_contains("/qa"))
time.sleep(1)

# language test ----------
language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
language_dropdown.click()
time.sleep(1)
language_chinese_cn = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[1]/a')
language_chinese_cn.click()
wait.until(EC.url_contains("/cn/qa"))
time.sleep(1)
language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
language_dropdown.click()
language_english = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[2]/a')
language_english.click()
wait.until(EC.url_contains("/en/qa"))
time.sleep(1)
language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
language_dropdown.click()
language_japanese = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[3]/a')
language_japanese.click()
wait.until(EC.url_contains("/jp/qa"))
time.sleep(1)
language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
language_dropdown.click()
language_chinese = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[4]/a')
language_chinese.click()
wait.until(EC.url_contains("/tw/qa"))
time.sleep(1)

# Search answer test -----------
question_input = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div[1]/div[2]/div/input')
question_input.send_keys('登入')
time.sleep(1)
search_result = browser.find_element(By.CLASS_NAME, 'question-collapse.open')
time.sleep(1)

# clean answer test ----------
clean_bt = browser.find_element(By.CLASS_NAME, 'btn-clean')
clean_bt.click()
time.sleep(1)
problem_category = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[3]')


# Search answer test -----------
question_input = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div[1]/div[2]/div/input')
question_input.send_keys('錢包')
time.sleep(1)
search_result = browser.find_element(By.CLASS_NAME, 'question-collapse.open')
time.sleep(1)