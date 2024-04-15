import requests
import pytest
import uuid
import csv
import time
from setting import send_email, generate_device_id, Enviroment



country_code = "TW"
# phone_number = f"09{random.randint(10000000, 99999999)}"
secret = str(uuid.uuid4())  # Replace with your actual client secret
global_sid = None
global_token = None
global_user_id = None
get_environment_url = Enviroment().get_base_url()
phone_number = Enviroment().get_phone_number()
env = Enviroment().env

@pytest.mark.run(order=1)
def test_register_msisdn():

    # API details
    url = f"{get_environment_url}/_matrix/client/r0/register/msisdn/requestCode"
    headers = {"Content-Type": "application/json"}

    # Request data
    data = {
        "country": country_code,
        "phone_number": phone_number,
        "client_secret": secret,
        "send_attempt": 1,
        "msisdn_use": "login"
    }

    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)

    # Make the POST request
    response = requests.post(url, json=data, headers=headers)

    # Validate the response
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "sid" in response_data, "Response does not contain 'sid'"
    assert "msg" in response_data, "Response does not contain 'msg'"
    assert response_data["msg"] == "success", f"Unexpected 'msg' value: {response_data['msg']}"
    
    #Extract session_id
    global global_sid
    global_sid = response_data.get("sid")

def write_to_csv():
    # 检查 global_token 是否存在
    if global_token is not None and global_user_id is not None and global_sid is not None:
        with open("token.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["token", global_token])
            writer.writerow(["user_id", global_user_id])
            writer.writerow(["sid", global_sid])
            writer.writerow(["client_secret", secret])
    else:
        print("Skipping writing to CSV.")
    

@pytest.mark.run(order=2)
def test_login():
    # API details
    url = f"{get_environment_url}/_matrix/client/r0/login/msisdnlogin"
    headers = {"Content-Type": "application/json"}
    device_id = generate_device_id()

    data = {
        "session_id": global_sid,
        "client_secret": secret,
        "code": "888888",
        "device_id": f"{device_id}",
        "initial_device_display_name": "IOS"
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)

    start_time = time.time()
    for i in range(1):
        response = requests.post(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    
    if diff_time > 5 or response.status_code != 200:
        send_email(f"[{env}][Login]", "login test failed please fix it.")
    else:
        print("Loading test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert ":shaberi.com" in response_data["user_id"], "Response does not contain 'user_id'"
    assert response_data["home_server"] == "shaberi.com", "Response does not contain 'home_sever'"
    assert "syt_" in response_data["access_token"], "Response does not contain 'access_token'" 
    assert "device_id" in response_data, "Response does not contain 'device_id'"
    
    if phone_number == "0975915790" :
        assert response_data["is_first"] == 0, "Response does not contain 'is_first'"
    else:
        pass
    
    #Extract access_token
    global global_token, global_user_id
    global_token = response_data.get("access_token")
    global_user_id = response_data.get("user_id")
    write_to_csv()
    
if __name__ == "__main__":
    pytest.main([__file__])







