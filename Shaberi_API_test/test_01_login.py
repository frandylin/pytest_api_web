import requests
import pytest
import uuid
import random
import csv


country_code = "TW"
phone_number = f"09{random.randint(10000000, 99999999)}"
secret = str(uuid.uuid4())  # Replace with your actual client secret
global_sid = None
global_token = None

def generate_device_id():
    # 生成 UUID
    device_id = uuid.uuid4()
    # 將 UUID 轉換為無連字符的16進位字串
    hex_string = str(device_id).replace('-', '')
    return hex_string[:32]

@pytest.mark.run(order=1)
def test_register_msisdn():

    # API details
    url = "https://im-stg.imdevs.net/_matrix/client/r0/register/msisdn/requestCode"
    headers = {"Content-Type": "application/json"}

    # Request data
    # country_code = "TW"
    # phone_number = f"09{random.randint(10000000, 99999999)}"
    # secret = str(uuid.uuid4())  # Replace with your actual client secret

    data = {
        "country": country_code,
        "phone_number": phone_number,
        "client_secret": secret,
        "send_attempt": 1,
        "msisdn_use": "login"
    }

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

# def extract_sid(response_data):
#     global global_sid
#     global_sid = response_data.get("sid")

def write_global_token_to_csv():
    # 检查 global_token 是否存在
    if global_token is not None:
        with open("token.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["token", global_token])
    else:
        print("global_token is None. Skipping writing to CSV.")


@pytest.mark.run(order=2)
def test_login():
    # API details
    url = "https://im-stg.imdevs.net/_matrix/client/r0/login/msisdnlogin"
    headers = {"Content-Type": "application/json"}
    device_id = generate_device_id()

    data = {
        "session_id": global_sid,
        "client_secret": secret,
        "code": "888888",
        "device_id": f"{device_id}",
        "initial_device_display_name": "IOS"
    }

    print("POST Data:" , data)
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    print("Response Data :" , response_data)
    assert ":shaberi.com" in response_data["user_id"], "Response does not contain 'user_id'"
    assert response_data["home_server"] == "shaberi.com", "Response does not contain 'home_sever'"
    assert "syt_" in response_data["access_token"], "Response does not contain 'access_token'" 
    assert "device_id" in response_data, "Response does not contain 'device_id'"
    assert response_data["is_first"] == 1, "Response does not contain 'is_first'"
    
    #Extract access_token
    global global_token
    global_token = response_data.get("access_token")
    write_global_token_to_csv()
    

if __name__ == "__main__":
    pytest.main([__file__])







