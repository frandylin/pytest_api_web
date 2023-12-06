from selenium import webdriver
import pytest
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

@pytest.fixture
def browser():
    # 初始化浏览器
    download_directory = os.path.expanduser('~/Downloads/unit_test_folder')
    os.makedirs(download_directory)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': download_directory,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': False,
        'safebrowsing.disable_download_protection': True,
    })
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    yield browser
    # 测试结束后关闭浏览器
    browser.quit()

def test_language_switching(browser):
    browser.get("https://www.shaberi.com/tw")
    wait = WebDriverWait(browser, 10)
    # language test-------------
    language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')

    def switch_language(language_element, expected_url_part):
        language_dropdown.click()
        language_element.click()
        wait.until(EC.url_contains(expected_url_part))
        time.sleep(1)

    # Test switching to Chinese (CN)
    switch_language(browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[1]/a'), "/cn")

    # Test switching to English
    switch_language(browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[2]/a'), "/en")

    # Test switching to Japanese
    switch_language(browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[3]/a'), "/jp")

    # Test switching back to Chinese (TW)
    switch_language(browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[4]/a'), "/tw")
