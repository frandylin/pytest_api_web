import requests
import pytest
import uuid
import random
import csv
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from datetime import datetime
from setting import get_environment_url
import hashlib
from setting import send_email, ReadCSV

#get variable
def get_variable():
    reader_csv = ReadCSV()
    reader_csv.read_csv()
    token = reader_csv.token
    user_id = reader_csv.user_id
    sid = reader_csv.sid
    client_secret = reader_csv.client_secret
    global global_token, global_user_id, global_sid, global_client_secret
    global_token = token
    global_user_id = user_id 
    global_sid = sid
    global_client_secret = client_secret

global_token = None
global_user_id = None 
global_sid = None
global_client_secret = None
global_wallet_password = None

@pytest.mark.run(order=3)
def test_wallet_config():

    # API details
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/wallet/config"
    headers = {"Content-Type": "application/json"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com" , "mac@twim.cc"]
    data = {

    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.get(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time

    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_email(f"[{env}][Wallet]", "wallet config test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert response_data["is_enable_wallet"] is True, "Wallet should be enabled"
    assert response_data["is_enable_deposit"] is True, "deposit should be enabled"
    assert response_data["is_enable_withdraw"] is True, "withdraw should be enabled"
    assert response_data["is_enable_red_packet"] is True, "red packet should be enabled"
    assert response_data["fee_of_deposit"] == 0.0, "Unexpected deposit fee"
    assert response_data["fee_of_withdraw"] == 0.0, "Unexpected withdraw fee"
    assert response_data["min_quota_of_withdraw"] == 10.0, "Unexpected min quota of withdraw"
    assert response_data["min_quota_of_send_red_packet"] == 0.01, "Unexpected min quota for sending red packet"
    assert response_data["max_quota_of_send_red_packet"] == 50.0, "Unexpected max quota for sending red packete"

@pytest.mark.run(order=4)
def test_wallet_setting_password():
    
    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/wallet/{global_user_id}/pay_password"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}

    #pre-request script
    password = "888888"
    data = f"{global_user_id}:{password}".encode('utf-8')
    wallet_password = hashlib.md5(data).hexdigest()
    global global_wallet_password
    global_wallet_password = wallet_password
    write_to_csv()
    data = {
        "wallet_password": f"{wallet_password}"
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.post(url, json=data, headers=headers)
        # Validate the response, 400 was already enable wallet status
        if response.status_code == 400 :
            assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        else:
            response_data = response.json()
            print("Response Data :" , response_data)
            assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
        
    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

@pytest.mark.run(order=5)
def test_wallet_information():

    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/wallet/{global_user_id}/wallet_info/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com", "mac@twim.cc"]
    data = {
        "erase": False,
        "auth": {
            "session": f"{global_sid}",
            "user": f"{global_user_id}",
            "sid": f"{global_sid}", 
            "client_secret": f"{global_client_secret}" 
        }        
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.get(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time

    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_email(f"[{env}][Wallet]", "wallet information test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")
    
    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    time.sleep(3)
    #ensure that three elements in the address_list
    response_list = response_data[0]
    assert len(response_list["address_list"]) == 3
    

@pytest.mark.run(order=6)
def test_wallet_records():

    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/wallet/{global_user_id}/records"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com", "mac@twim.cc"]
    data = {

    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.get(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time

    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_email(f"[{env}][Wallet]", "wallet records test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")
    
    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

    assert "total" in response_data, "Response does not contain 'total'"
    assert "current_page" in response_data, "Response does not contain 'current_page'"
    assert response_data["per_page"] == 20, "Response does not equal 20"
    assert "data" in response_data, "Response does not contain 'data'"

def write_to_csv():
    # 检查 global_token 是否存在
    if global_wallet_password is not None:
        # "a" 模式代表 append ，文件存在的話將在文件尾段加入新的一行
        with open("token.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["wallet_password", global_wallet_password])
    else:
        print("Skipping writing to CSV.")

if __name__ == "__main__":


    pytest.main([__file__])







