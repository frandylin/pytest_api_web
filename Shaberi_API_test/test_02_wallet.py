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
from setting import send_email

global_token = None
global_user_id = None

def read_csv():
    global global_token, global_user_id
    with open("token.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == "token":
                global_token = row[1]
            elif row[0] == "user_id":
                global_user_id = row[1]

@pytest.mark.run(order=3)
def test_wallet_config():

    # API details
    url = f"{urls['prod']}/_matrix/client/r0/wallet/config"
    headers = {"Content-Type": "application/json"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com", "xuan@twim.cc"]
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
    if diff_time < 5:
        print("Loading test passed. ")
    else:
        send_email("", "wallet config test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")

    if response.status_code != 200:
        send_email("", "wallet config test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        pass

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
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

    read_csv()
    # API details
    url = f"{urls['prod']}/_matrix/client/r0/wallet/{global_user_id}/pay_password"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}

    #pre-request script
    password = "888888"
    data = f"{global_user_id}:{password}".encode('utf-8')
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
        # Validate the response
        if response.status_code == 400 :
            assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        else:
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        
    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    end_time = time.time()
    diff_time = end_time - start_time




if __name__ == "__main__":

    pytest.main([__file__])







