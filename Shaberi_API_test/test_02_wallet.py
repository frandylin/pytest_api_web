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
from setting import get_environment_wallet_url
import hashlib
from setting import send_email, ReadCSV

#get variable
def get_variable():
    reader_csv = ReadCSV()
    reader_csv.read_csv()
    global global_token, global_user_id, global_sid, global_client_secret
    global_token = reader_csv.token
    global_user_id = reader_csv.user_id
    global_sid = reader_csv.sid
    global_client_secret = reader_csv.client_secret


global_token = None
global_user_id = None 
global_sid = None
global_client_secret = None
global_wallet_password = None
global_wallet_address = None
global_wallet_record_id = None

@pytest.mark.run(order=3)
def test_wallet_config():

    # API details
    env = "uat"
    url = f"{get_environment_wallet_url(env)}/_matrix/client/r0/wallet/config"
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com" , "mac@twim.cc"]

    print("url:" , url)
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.get(url)
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
    url = f"{get_environment_wallet_url(env)}/_matrix/client/r0/wallet/{global_user_id}/pay_password"
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
    url = f"{get_environment_wallet_url(env)}/_matrix/client/r0/wallet/{global_user_id}/wallet_info/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com", "mac@twim.cc"]
 
    print("url:" , url)
    print("header:" , headers)
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.get(url,  headers=headers)
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
    time.sleep(5)
    #ensure that three elements in the address_list
    response_list = response_data[0]
    assert len(response_list["address_list"]) == 3
    

@pytest.mark.run(order=6)
def test_wallet_records():

    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_wallet_url(env)}/_matrix/client/r0/wallet/{global_user_id}/records"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com", "mac@twim.cc"]
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" )
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.get(url, headers=headers)
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
    global global_wallet_record_id
    global_wallet_record_id = response_data.get("data", [])[0]["wallet_record_id"]

@pytest.mark.run(order=7)
def test_wallet_single_records():

    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_wallet_url(env)}/_matrix/client/r0/wallet/{global_user_id}/records/{global_wallet_record_id}/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" )
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.get(url, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    
    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "wallet_record_id" in response_data, "Response does not contain 'wallet_recoed_id'"
    assert "bill_no" in response_data, "Response does not contain 'bill_no'"
    assert "create_at" in response_data, "Response does not contain 'create_at'"
    assert "tran_amount" in response_data, "Response does not contain 'tran_amount'"
    assert "balance_amount" in response_data, "Response does not contain 'balance_amount'"

@pytest.mark.run(order=8)
def test_wallet_address():

    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_wallet_url(env)}/_matrix/client/r0/wallet/{global_user_id}/wallet_address"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com", "mac@twim.cc"]
    data = {
        "name": "frandy api test",
        "address": "0x000000",
        "protocol": "ERC20"
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(1):
        # Make the POST requests
        response = requests.post(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time

    #testing loading time
    if diff_time > 5 or response.status_code != 201:
        send_email(f"[{env}][Wallet]", "wallet address test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")
    
    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    global global_wallet_address
    global_wallet_address = response_data.get("shortcut_wallet_id")

    assert "shortcut_wallet_id" in response_data, "Response does not contain 'shortcut_wallet_id'"

@pytest.mark.run(order=9)
def test_wallet_address_change():

    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_wallet_url(env)}/_matrix/client/r0/wallet/{global_user_id}/wallet_address/{global_wallet_address}/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com", "mac@twim.cc"]
    data = {
        "name": "frandy api test change",
        "address": "0x000000",
        "protocol": "ERC20"
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(1):
        # Make the POST requests
        response = requests.put(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time

    #testing loading time
    if diff_time > 5 or response.status_code != 202:
        send_email(f"[{env}][Wallet]", "wallet address change test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")
    
    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 202, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

    assert response_data["msg"] == 1, "Response does not contain 'msg'"

@pytest.mark.run(order=10)
def test_wallet_address_delete():

    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_wallet_url(env)}/_matrix/client/r0/wallet/{global_user_id}/wallet_address/{global_wallet_address}/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com", "mac@twim.cc"]
    data = {
        "name": "frandy api test change",
        "address": "0x000000",
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(1):
        # Make the POST requests
        response = requests.delete(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time

    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_email(f"[{env}][Wallet]", "wallet address delete test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")
    
    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

    assert response_data["msg"] == 1, "Response does not contain 'msg'"

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







