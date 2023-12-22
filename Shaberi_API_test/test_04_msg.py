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
room_id = "!269249103520:shaberi.com"

@pytest.mark.run(order=8)
def test_create_room():

    # API details
    url = f"{urls['prod']}/_matrix/client/r0/{room_id}/send/m.room.message/m{timestamp}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com"]
    data = {
        "msgtype": "m.text",
        "body": "frandy testinggggggg"
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
        send_email("[Room]", "send message test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("send message test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "$" in response_data["event_id"], "Response does not contain 'event_id'"

if __name__ == "__main__":


    pytest.main([__file__])







