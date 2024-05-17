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
        ('简体中文', '/cn/privacy'),
        ('English', '/en/privacy'),
        ('日本語', '/jp/privacy'),
        ('繁體中文', '/tw/privacy')
    ]

    for lang, expected_url_part in languages:
        language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
        language_dropdown.click()
        language_option = browser.find_element(By.XPATH, f'//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li/a[contains(text(), "{lang}")]')
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