import requests
import pytest
import time
import os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from datetime import datetime
from setting import get_environment_url
from setting import send_email, ReadCSV

#get variable
def get_variable():
    reader_csv = ReadCSV()
    reader_csv.read_csv()
    token = reader_csv.token
    user_id = reader_csv.user_id
    wallet_password = reader_csv.wallet_password
    global global_token, global_user_id
    global_token = token
    global_user_id = user_id 

global_token = None
global_user_id = None 

@pytest.mark.run(order=19)
def test_revise_displayname():

    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/profile/{global_user_id}/displayname"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com"]
    data = {
        "displayname": "testfrandy",
    }   
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    # Make the POST requests
    response = requests.put(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 10 or response.status_code != 200:
        send_email(f"[{env}][Personal]", "revise displayname test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("send message test passed. ")

    # Validate the response
    assert diff_time < 10, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

@pytest.mark.run(order=20)
def test_change_avatar():
    image_folder = os.path.join(os.path.dirname(__file__), 'assets')
    image = os.path.join(image_folder, "pepe.jpeg")
    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/profile/{global_user_id}/avatar_url"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com"]
    with open(image, "rb") as image_file:
        data = {
            "avatar_url": image
        }   
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    # Make the POST requests
    response = requests.put(url, json=data, headers=headers)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

@pytest.mark.run(order=21)
def test_search_profile():

    # API details
    get_variable()
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/profile/{global_user_id}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    recipients_list = ["genman@twim.cc", "frandyfancy@gmail.com"]
    print("url:" , url)
    print("header:" , headers)
    start_time = time.time()
    # Make the POST requests
    response = requests.get(url, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 10 or response.status_code != 200:
        send_email(f"[{env}][Personal]", "search profile test failed please fix it.", "frandyfancy@gmail.com", recipients_list, "xjbtujjvqkywrslh")
    else:
        print("send message test passed. ")

    # Validate the response
    assert diff_time < 10, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "displayname" in response_data, "Response does not contain 'displayname'"
    assert "introduction" in response_data, "Response does not contain 'introduction'"
    assert "avatar_url" in response_data, "Response does not contain 'avatar_url'"
    assert "user_name" in response_data, "Response does not contain 'user_name'"
    assert "phone_number" in response_data, "Response does not contain 'phone_number'"



if __name__ == "__main__":


    pytest.main([__file__])







