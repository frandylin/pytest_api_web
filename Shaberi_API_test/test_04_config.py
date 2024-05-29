import requests
import pytest
import time
from setting import ReadCSV, Enviroment, send_signal_message

#get variable
def get_variable():
    reader_csv = ReadCSV()
    reader_csv.read_csv()
    global global_token, global_user_id
    global_token = reader_csv.token
    global_user_id = reader_csv.user_id
global_token = None
global_user_id = None

get_environment_url = Enviroment().get_base_url()
env = Enviroment().env
current_time = int(time.time())
app_version = "2.1.12"
app_min_version = "2.1.12"
desktop_version = "2.0.7"
desktop_min_version = "1.0.0"

def search_version(user_os):
#1: android, 2: android中國版, 3:ios, 4 ios中國版, 5:win, 6:mac
    
    #API details
    get_variable()
    url = f"{get_environment_url}/_matrix/client/r0/system/{user_os}/version"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    print("url:", url)
    print("header:", url)
    #Make the post requests
    response = requests.get(url, headers=headers)
    
    #Validate the response
    assert response.status_code ==200, f"Unexpected status code: {response.status_code}"

    #Assuming the response body is in JSON format
    response_data = response.json()
    print("response_data:", response_data)
    return response_data

@pytest.mark.run(order=21)
def test_search_version_android():
    response_data = search_version(1)
    assert response_data["platform"] == 1, "android platform was not correct."
    assert response_data["version"] == app_version, "android version was not correct"
    assert response_data["min_version"] == app_min_version, "android min_version was not correct."
    assert "description" in response_data, "Response dose not contain 'description'"
    assert response_data["url"] == "https://play.google.com/store/apps/details?id=jp.primetheory.talktalk", "android url was not correct"

@pytest.mark.run(order=22)
def test_search_version_android_china():
    response_data = search_version(2)
    assert response_data["platform"] == 2, "android china platform was not correct."
    assert response_data["version"] == app_version, "android china version was not correct"
    assert response_data["min_version"] == app_min_version, "android china min_version was not correct."
    assert "description" in response_data, "Response dose not contain 'description'"
    if env == "prod":
        assert f"https://im-upload-media.s3.ap-east-1.amazonaws.com/prod/admin_file/SB_v{app_version}_fdroid" in response_data["url"], "android china url was not correct"
    else:
        pass
    
@pytest.mark.run(order=23)
def test_search_version_ios():
    response_data = search_version(3)
    assert response_data["platform"] == 3, "ios platform was not correct."
    assert response_data["version"] == app_version, "ios version was not correct"
    assert response_data["min_version"] == app_min_version, "ios min_version was not correct."
    assert "description" in response_data, "Response dose not contain 'description'"
    assert response_data["url"] == "https://apps.apple.com/tw/app/shaberi/id1640215709", "ios url was not correct"
    
@pytest.mark.run(order=24)
def test_search_version_ios_china():
    response_data = search_version(4)
    assert response_data["platform"] == 4, "ios china platform was not correct."
    assert response_data["version"] == app_version, "ios china version was not correct"
    assert response_data["min_version"] == app_min_version, "ios china min_version was not correct."
    assert "description" in response_data, "Response dose not contain 'description'"
    assert response_data["url"] == "https://apps.apple.com/us/app/%E8%99%BE%E8%B4%9D/id6451127792", "ios china url was not correct"
    
@pytest.mark.run(order=25)
def test_search_version_windows():
    response_data = search_version(5)
    assert response_data["platform"] == 5, "windows platform was not correct."
    assert response_data["version"] == desktop_version, "windows version was not correct"
    assert response_data["min_version"] == desktop_min_version, "wiindows min_version was not correct."
    assert "description" in response_data, "Response dose not contain 'description'"
    if env == "prod":
        assert response_data["url"] == f"https://im-upload-media.s3.ap-east-1.amazonaws.com/prod/admin_file/Shaberi_Setup_{desktop_version}.exe", "windows url was not correct"
    else:
        pass

@pytest.mark.run(order=26)
def test_search_version_mac():
    response_data = search_version(6)
    assert response_data["platform"] == 6, "mac platform was not correct."
    assert response_data["version"] == desktop_version, "mac version was not correct"
    assert response_data["min_version"] == desktop_min_version, "mac min_version was not correct."
    assert "description" in response_data, "Response dose not contain 'description'"
    if env == "prod":
        assert response_data["url"] == f"https://im-upload-media.s3.ap-east-1.amazonaws.com/prod/admin_file/Shaberi-{desktop_version}-universal.dmg", "mac url was not correct"
    else:
        pass

@pytest.mark.run(order=27)
def test_search_version_mac_applestore():
    response_data = search_version(7)
    assert response_data["platform"] == 7, "mac platform was not correct."
    assert response_data["version"] == desktop_version, "mac version was not correct"
    assert response_data["min_version"] == desktop_min_version, "mac min_version was not correct."
    assert "description" in response_data, "Response dose not contain 'description'"
    assert response_data["url"] == "https://apps.apple.com/us/app/shaberi-desktop/id6475802962", "mac apple store url was not correct"

@pytest.mark.run(order=28)
def test_announce_message():

    # API details
    get_variable()
    url = f"{get_environment_url}/_matrix/client/r0/system/board?update_ts={current_time}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    print("url:" , url)
    print("header:" , headers)
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.get(url, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_signal_message(f"{env} [Room]\nannounce message test failed please fix it.")
    else:
        print("Loading test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "event_id" in response_data["events"][0], "Response does not contain 'event_id"
    assert "content" in response_data["events"][0], "Response does not contain 'content"
    assert "origin_server_ts" in response_data["events"][0], "Response does not contain 'origin_server_ts"
    assert "type" in response_data["events"][0], "Response does not contain'type"
    assert "sender" in response_data["events"][0], "Response does not contain'sender"
    assert "is_show" in response_data["events"][0], "Response does not contain'is_show"