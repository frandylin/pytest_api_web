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

@pytest.fixture(scope='session')
def browser():
    download_directory = os.path.expanduser('~/Downloads/unit_test_folder')
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': download_directory,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': False,
        'safebrowsing.disable_download_protection': True,
    })
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    ### 初始化 ###
    # [建立]測試資料
    os.makedirs(download_directory)
    yield driver
    driver.quit()

@pytest.mark.run(order=1)
def test_privacy_page(browser):
    browser.get("https://www.shaberi.com/tw")
    
    # main page test
    wait = WebDriverWait(browser, 10)
    wait.until(EC.url_contains("www.shaberi.com"))
    time.sleep(1)

    # Add assertion
    assert "www.shaberi.com" in browser.current_url

@pytest.mark.run(order=2)
def test_language_switch(browser):

    languages = [
        ('简体中文', '/cn'),
        ('English', '/en'),
        ('日本語', '/jp'),
        ('繁體中文', '/tw')
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

def wait_until_new_window(browser):
    wait = WebDriverWait(browser, 10)
    wait.until(lambda browser: len(browser.window_handles) > 1)

def switch_to_new_window(browser):
    browser.switch_to.window(browser.window_handles[1])

def switch_to_main_window(browser):
    browser.switch_to.window(browser.window_handles[0])

@pytest.mark.run(order=3)
def test_download_links(browser):
    wait = WebDriverWait(browser, 10)
        # Apple Store
    apple_store = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[1]/div/a[1]')
    apple_store.click()
    wait_until_new_window(browser)
    switch_to_new_window(browser)
    wait.until(EC.url_to_be("https://apps.apple.com/tw/app/shaberi/id1640215709"))
    assert "https://apps.apple.com/tw/app/shaberi/id1640215709" in browser.current_url
    browser.close()

    # Google Play
    switch_to_main_window(browser)
    google_play = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[1]/div/a[2]')
    google_play.click()
    wait_until_new_window(browser)
    switch_to_new_window(browser)
    wait.until(EC.url_to_be("https://play.google.com/store/apps/details?id=jp.primetheory.talktalk"))
    assert "https://play.google.com/store/apps/details?id=jp.primetheory.talktalk" in browser.current_url
    browser.close()

    # Apple Store CN
    switch_to_main_window(browser)
    apple_store_cn = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[2]/div/a[1]')
    apple_store_cn.click()
    wait_until_new_window(browser)
    switch_to_new_window(browser)
    wait.until(EC.url_to_be("https://apps.apple.com/us/app/%E8%99%BE%E8%B4%9D/id6451127792"))
    assert "https://apps.apple.com/us/app/%E8%99%BE%E8%B4%9D/id6451127792" in browser.current_url
    browser.close()

    # Switch back to the main window
    switch_to_main_window(browser)

@pytest.mark.run(order=4)
def test_apk_download(browser):
    print("Testing Android APK download URL")
    download_directory = os.path.expanduser('~/Downloads/unit_test_folder')
    apk_bt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[2]/div/a[2]')
    apk_bt.click()
    apk_url = apk_bt.get_attribute("href").split("/")[-1]

    try:
        # 等待下载完成，最多等待40秒
        wait_time = 0
        is_download_ok = False
        while wait_time < 40 and not is_download_ok:
            if wait_time % 5 == 0:
                print(f"等待時間 {wait_time}")
            
            downloaded_files = os.listdir(download_directory)
            for files in downloaded_files:
                if "apk" in files:
                    print(f"找到的檔案有 {files}")
                if apk_url == files.split("/")[-1]:
                    print("[PASS]")
                    print("apk_url:", apk_url)
                    is_download_ok = True
                    break
            
            if not is_download_ok:
                wait_time += 1
                time.sleep(1)
        
        assert is_download_ok, "APK 下載失敗"

    except Exception as e:
        print(f"錯誤: {e}")
        raise
    finally:
        pass

@pytest.mark.run(order=5)
def test_macos_download(browser):
    print("Testing macOS download URL")
    download_directory = os.path.expanduser('~/Downloads/unit_test_folder')
    macos_bt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[3]/div/a[1]')
    macos_bt.click()
    time.sleep(1)
    macos_url = "crdownload"

    try:
        # 等待下载完成，最多等待10秒
        wait_time = 0
        macos_is_download_ok = False
        while wait_time < 10 and not macos_is_download_ok:
            if wait_time % 5 == 0:
                print(f"等待時間 {wait_time}")
            
            downloaded_files = os.listdir(download_directory)
            for files in downloaded_files:
                if "crdownload" in files:
                    print(f"找到的檔案有 {files}")
                if macos_url in files:
                    print("[PASS]")
                    print("macos_url:", macos_url)
                    macos_is_download_ok = True
                    break
            
            if not macos_is_download_ok:
                wait_time += 1
                time.sleep(1)
        
        assert macos_is_download_ok, "macOS 下載失敗"

    except Exception as e:
        print(f"錯誤: {e}")
        raise
    finally:
        pass

@pytest.mark.run(order=6)
def test_windows_download(browser):
    print("Testing Windows download URL")
    download_directory = os.path.expanduser('~/Downloads/unit_test_folder')
    windows_bt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[3]/div/a[2]')
    windows_bt.click()
    windows_url = windows_bt.get_attribute("href").split("/")[-1]
    print(windows_url)

    try:
        # 等待下载完成，最多等待40秒
        wait_time = 0
        windows_is_download_ok = False
        while wait_time < 40 and not windows_is_download_ok:
            if wait_time % 5 == 0:
                print(f"等待時間 {wait_time}")
            
            downloaded_files = os.listdir(download_directory)
            for files in downloaded_files:
                if "exe" in files:
                    print(f"找到的檔案有 {files}")
                if windows_url == files.split("/")[-1]:
                    print("[PASS]")
                    print("windows_url:", windows_url)
                    windows_is_download_ok = True
                    break
            
            if not windows_is_download_ok:
                wait_time += 1
                time.sleep(1)
        
        assert windows_is_download_ok, "Windows 下載失敗"

    except Exception as e:
        print(f"錯誤: {e}")
        raise
    finally:
        pass
        # [刪除]測試資料
        shutil.rmtree(download_directory)

@pytest.mark.run(order=7)
def test_twitter(browser):
    print("Testing Twitter link")
    wait = WebDriverWait(browser, 10)
    twitter_bt = browser.find_element(By.CLASS_NAME, 'download-link.pr-6')
    actions = ActionChains(browser)
    actions.move_to_element(twitter_bt).perform()
    twitter_bt.click()
    wait_until_new_window(browser)
    switch_to_new_window(browser)
    wait.until(EC.url_contains("https://twitter.com/"))
    assert "https://twitter.com/" in browser.current_url
    # Add more assertions if needed, e.g., check for elements on the Twitter login page
    browser.close()
    browser.switch_to.window(browser.window_handles[0])