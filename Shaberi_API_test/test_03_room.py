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

@pytest.mark.run(order=7)
def test_create_room():

    # API details
    url = f"{urls['prod']}/_matrix/client/r0/createRoom"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com"]
    data = {
        "name": "frandytest",
        "preset": "private_chat",
        "invite": [],
        "visibility": "private",
        "initial_state": [
            {
                "type": "m.room.encryption",
                "state_key": "",
                "content": {
                    "algorithm": null
                }
            }
        ]
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
        send_email("[Room]", "create room test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("Loading test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert ":shaberi.com" in response_data["room_id"], "Response does not contain 'room_id'"

if __name__ == "__main__":


    pytest.main([__file__])







