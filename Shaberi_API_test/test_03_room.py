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

reader_csv = ReadCSV()
reader_csv.read_csv()
token = reader_csv.token
user_id = reader_csv.user_id
sid = reader_csv.sid
client_secret = reader_csv.client_secret
wallet_password = reader_csv.wallet_password
global_room_id = None
global_red_packet_id = None

@pytest.mark.run(order=7)
def test_create_room():

    # API details
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/createRoom"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com"]
    data = {
        "name": "apitest",
        "preset": "private_chat",
        "invite": [],
        "visibility": "private",
        "initial_state": [
            {
                "type": "m.room.encryption",
                "state_key": "",
                "content": {
                    "algorithm": None
                }
            }
        ]
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
    if diff_time > 5 or response.status_code != 200:
        send_email(f"[{env}][Room]", "create room test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert ":shaberi.com" in response_data["room_id"], "Response does not contain 'room_id'"
    #Extract session_id
    global global_room_id
    global_room_id = response_data.get("room_id")

@pytest.mark.run(order=8)
def test_send_packet():

    # API details
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/wallet/{user_id}/rooms/{global_room_id}/red_packet"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com"]
    total_amount = "0.010"
    count = 1
    fee = "0.000"
    red_packet_type = 10
    key = "shaberi_key_2023"
    
    print(f"{wallet_password}:{user_id}:{total_amount}:{fee}:{count}:{red_packet_type}:{global_room_id}:{key}")
    data_hash = f"{wallet_password}:{user_id}:{total_amount}:{fee}:{count}:{red_packet_type}:{global_room_id}:{key}".encode('utf-8')
    wallet_sign = hashlib.md5(data_hash).hexdigest()
    data = {
        #1 是單人 10 群組隨機 11群組固定
        "red_packet_type": red_packet_type, 
        "count": count,
        "total_amount": total_amount,
        "note": "恭喜發財 😂",
        "sign":f"{wallet_sign}",
        "fee": fee
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

    # #testing loading time
    # if diff_time > 5 or response.status_code != 200:
    #     send_email("[Room]", "send red packet test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    # else:
    #     print("Loading test passed. ")

    # Validate the response
    response_data = response.json()
    print("Response Data :" , response_data)
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    # Assuming the response body is in JSON format
    assert "balance_amount" in response_data, "Response does not contain 'balance_amount'"
    assert "fee" in response_data, "Response does not contain 'fee'"
    assert "expire_at" in response_data, "Response does not contain 'expire_at'"
    assert "red_packet_id" in response_data, "Response does not contain 'red_packet_id'"
    global global_red_packet_id
    global_red_packet_id = response_data.get("red_packet_id")

@pytest.mark.run(order=9)
def test_receive_packet():

    # API details
    url = f"{urls['uat']}/_matrix/client/r0/wallet/{user_id}/rooms/{global_room_id}/red_packet/{global_red_packet_id}/claim"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com"]

    data = {

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

    # #testing loading time
    # if diff_time > 5 or response.status_code != 200:
    #     send_email("[Room]", "send red packet test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    # else:
    #     print("Loading test passed. ")

    # Validate the response
    response_data = response.json()
    print("Response Data :" , response_data)
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    assert "balance_amount" in response_data, "Response does not contain 'balance_amount'"
    assert "tran_amount" in response_data, "Response does not contain 'tran_amount'"
    assert "remain" in response_data, "Response does not contain 'remain'"
    assert "claim_count" in response_data, "Response does not contain 'claim_count'"

@pytest.mark.run(order=10)
def test_leave_room():

    # API details
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/rooms/{global_room_id}/leave"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com"]
    data = {

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

    # testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_email(f"[{env}][Room]", "leave room test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)


if __name__ == "__main__":


    pytest.main([__file__])







