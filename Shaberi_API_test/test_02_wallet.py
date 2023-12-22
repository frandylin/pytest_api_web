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
from setting import urls
import hashlib
from setting import send_email, ReadCSV

reader_csv = ReadCSV()
reader_csv.read_csv()
token = reader_csv.token
user_id = reader_csv.user_id
sid = reader_csv.sid
client_secret = reader_csv.client_secret

@pytest.mark.run(order=3)
def test_wallet_config():

    # API details
    url = f"{urls['prod']}/_matrix/client/r0/wallet/config"
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
        send_email("[Wallet]", "wallet config test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
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
    url = f"{urls['prod']}/_matrix/client/r0/wallet/{user_id}/pay_password"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    #pre-request script
    password = "888888"
    data = f"{user_id}:{password}".encode('utf-8')
    wallet_password = hashlib.md5(data).hexdigest()
    # wallet_password = "b7fefe2e27e59da60142aa41dc656fa9"

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
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        
    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

@pytest.mark.run(order=5)
def test_wallet_information():
    
    # API details
    url = f"{urls['prod']}/_matrix/client/r0/wallet/{user_id}/wallet_info/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com", "mac@twim.cc"]
    data = {
        "erase": False,
        "auth": {
            "session": f"{sid}",
            "user": f"{user_id}",
            "sid": f"{sid}", 
            "client_secret": f"{client_secret}"  
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
        send_email("[Wallet]", "wallet information test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")
    
    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    #ensure that three elements in the address_list
    assert len(response_data["address_list"]) == 3
    

@pytest.mark.run(order=6)
def test_wallet_records():
    
    # API details
    url = f"{urls['prod']}/_matrix/client/r0/wallet/{user_id}/records"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com", "mac@twim.cc"]
    data = {

    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(1):
        # Make the POST requests
        response = requests.get(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time

    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_email("[Wallet]", "wallet records test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")
    
    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

    assert "total" in response_data["total"], "Response does not contain 'total'"
    assert "current_page" in response_data["current_page"], "Response does not contain 'current_page'"
    assert response_data["per_page"] == 20, "Response does not equal 20"
    assert "data" in response_data["data"], "Response does not contain 'data'"










if __name__ == "__main__":


    pytest.main([__file__])







