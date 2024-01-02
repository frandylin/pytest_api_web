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
    wallet_password = reader_csv.wallet_password
    global global_token, global_user_id, global_wallet_password
    global_token = token
    global_user_id = user_id 

global_token = None
global_user_id = None 

room_id = "!299555311424:shaberi.com"

@pytest.mark.run(order=11)
def test_send_message():

    current_time = int(time.time())
    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/rooms/{room_id}/send/m.room.message/m{current_time}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com"]
    data = {
        "msgtype": "m.text",
        "body": "frandy"
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.put(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 10 or response.status_code != 200:
        send_email(f"[{env}][Message]", "send message test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("send message test passed. ")

    # Validate the response
    assert diff_time < 10, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "$" in response_data["event_id"], "Response does not contain 'event_id'"

if __name__ == "__main__":


    pytest.main([__file__])







