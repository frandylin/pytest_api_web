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

### 初始化 ###
download_directory = os.path.expanduser('~/Downloads/unit_test_folder')
# [建立]測試資料
os.makedirs(download_directory)

chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_directory,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': False,
    'safebrowsing.disable_download_protection': True,
})
browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window()
wait = WebDriverWait(browser, 10)
actions = ActionChains(browser)
current_url = browser.current_url


### 正式開始測試 ### 
browser.get("https://www.shaberi.com/tw")


# language test-------------
language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
language_dropdown.click()
language_chinese_cn = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[1]/a')
language_chinese_cn.click()
wait.until(EC.url_contains("/cn"))
time.sleep(1)
language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
language_dropdown.click()
language_english = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[2]/a')
language_english.click()
wait.until(EC.url_contains("/en"))
time.sleep(1)
language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
language_dropdown.click()
language_japanese = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[3]/a')
language_japanese.click()
wait.until(EC.url_contains("/jp"))
time.sleep(1)
language_dropdown = browser.find_element(By.CLASS_NAME, 'flex.cursor-pointer')
language_dropdown.click()
language_chinese = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/header/div[1]/div/div/div/ul/li[4]/a')
language_chinese.click()
wait.until(EC.url_contains("/tw"))
time.sleep(1)

#download test -----------
apple_store = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[1]/div/a[1]')
apple_store.click()
wait.until(lambda browser : len(browser.window_handles) > 1)
browser.switch_to.window(browser.window_handles[1])
wait.until(EC.url_to_be("https://apps.apple.com/tw/app/shaberi/id1640215709"))
browser.close()

browser.switch_to.window(browser.window_handles[0])
google_play = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[1]/div/a[2]')
google_play.click()
wait.until(lambda brower : len(browser.window_handles) > 1)
browser.switch_to.window(browser.window_handles[1])
wait.until(EC.url_to_be("https://play.google.com/store/apps/details?id=jp.primetheory.talktalk"))
browser.close()

browser.switch_to.window(browser.window_handles[0])
apple_store_cn = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[2]/div/a[1]')
apple_store_cn.click()
wait.until(lambda brower : len(browser.window_handles) > 1)
browser.switch_to.window(browser.window_handles[1])
wait.until(EC.url_to_be("https://apps.apple.com/us/app/%E8%99%BE%E8%B4%9D/id6451127792"))
browser.close()
browser.switch_to.window(browser.window_handles[0])

print("testing android apk download url")
time.sleep(1)
apk_bt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[2]/div/a[2]')
apk_bt.click()
apk_url = apk_bt.get_attribute("href").split("/")[-1]
try:
    # 等待下载完成，最多等待10秒
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
                print("apk_url:",apk_url)
                is_download_ok = True                                
                break
        if not is_download_ok:
            wait_time += 1
            time.sleep(1)
    if not is_download_ok:
        print("[Fail] ")
finally:
    pass

print("testing macos download url")
macos_bt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[3]/div/a[1]')
macos_bt.click()
time.sleep(1)
# macos_url = macos_bt.get_attribute("href").split("/")[-1]
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
                print("macos_url:",macos_url)
                macos_is_download_ok = True
                break
        if not macos_is_download_ok:
            wait_time += 1
            time.sleep(1)
    if not macos_is_download_ok:
        print("[Fail]")
finally:
    pass


print("testing windows download url")
windows_bt = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/section[1]/div/div[1]/div/div[3]/div/a[2]')
windows_bt.click()
windows_url = windows_bt.get_attribute("href").split("/")[-1]
print(windows_url)
try:
    # 等待下载完成，最多等待10秒
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
                print("windows_url:",windows_url)
                windows_is_download_ok = True
                break
        if not windows_is_download_ok:
            wait_time += 1
            time.sleep(1)
    if not windows_is_download_ok:
        print("[Fail] ")
finally:
    pass

# [刪除]測試資料
shutil.rmtree(download_directory)

#Twitter test ------
twitter_bt = browser.find_element(By.CLASS_NAME, 'inline.hover:underline')
actions = ActionChains(browser)
actions.move_to_element(twitter_bt).perform()
twitter_bt.click()
wait.until(lambda browser : len(browser.window_handles) > 1)
browser.switch_to.window(browser.window_handles[1])
wait.until(EC.url_to_be("https://twitter.com/i/flow/login?redirect_after_login=%2Ftalktal36600622"))
browser.close()
