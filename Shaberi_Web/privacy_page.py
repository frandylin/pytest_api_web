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
import pytest


# browser = webdriver.Chrome()
# browser.maximize_window()
# wait = WebDriverWait(browser, 10)
# actions = ActionChains(browser)
# current_url = browser.current_url

# ### 正式開始測試 ### 
# browser.get("https://www.shaberi.com/tw")

# #privacy page test --------------
# privacy_bt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/ul/li[3]/a')
# privacy_bt.click()
# wait.until(EC.url_contains("/privacy"))
# time.sleep(1)

# # language test ----------
# language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
# language_dropdown.click()
# time.sleep(1)
# language_chinese_cn = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[1]/a')
# language_chinese_cn.click()
# wait.until(EC.url_contains("/cn/"))
# time.sleep(1)
# language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
# language_dropdown.click()
# language_english = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[2]/a')
# language_english.click()
# wait.until(EC.url_contains("/en/privacy"))
# time.sleep(1)
# language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
# language_dropdown.click()
# language_japanese = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[3]/a')
# language_japanese.click()
# wait.until(EC.url_contains("/jp/privacy"))
# time.sleep(1)
# language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
# language_dropdown.click()
# language_chinese = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[4]/a')
# language_chinese.click()
# wait.until(EC.url_contains("/tw/privacy"))
# time.sleep(5)

# #Callapse test ----------
# callapse_01 = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div[1]')
# callapse_01.click()
# time.sleep(1)

# callapse_02 = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div[1]')
# callapse_02.click()
# time.sleep(1)

# callapse_03 = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[3]/div[1]')
# callapse_03.click()
# time.sleep(1)

# callapse_04 = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[4]/div[1]')
# callapse_04.click()
# time.sleep(1)

# callapse_05 = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]')
# callapse_05.click()
# time.sleep(1)

# callapse_06 = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[6]/div[1]')
# callapse_06.click()
# time.sleep(1)


@pytest.fixture(scope='session')
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.run(order=1)
def test_privacy_page(browser):
    browser.get("https://www.shaberi.com/tw")
    
    # privacy page test
    privacy_bt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/ul/li[3]/a')
    privacy_bt.click()
    wait = WebDriverWait(browser, 10)
    wait.until(EC.url_contains("/privacy"))
    time.sleep(1)

    # Add assertion
    assert "/privacy" in browser.current_url

@pytest.mark.run(order=2)
def test_language_switch(browser):

    languages = [
        ('1', '/cn/privacy'),
        ('2', '/en/privacy'),
        ('3', '/jp/privacy'),
        ('4', '/tw/privacy')
    ]

    for lang, expected_url_part in languages:
        language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
        language_dropdown.click()
        language_option = browser.find_element(By.XPATH, f'//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[{lang}]/a')
        language_option.click()
        wait = WebDriverWait(browser, 10)
        wait.until(EC.url_contains(expected_url_part))
        time.sleep(1)

        # Add assertion
        assert expected_url_part in browser.current_url

@pytest.mark.run(order=3)
def test_collapse_elements(browser):

    # Callapse test
    for i in range(1, 7):
        collapse_element = browser.find_element(By.XPATH, f'//*[@id="__layout"]/div/div[2]/div[{i}]/div[1]')
        collapse_element.click()
        time.sleep(1)

        # Add assertion
        assert "collapse" in collapse_element.get_attribute("class")