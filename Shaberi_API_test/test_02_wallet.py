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

def read_global_token_from_csv():
    with open("token.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == "token":
                return row[1]
                  
# token = read_global_token_from_csv()  

@pytest.mark.run(order=3)
def test_wallet_config():

    # API details
    url = "https://im-stg.imdevs.net/_matrix/client/r0/wallet/config"
    # headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    headers = {"Content-Type": "application/json"}
    data = {

    }
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.get(url, json=data, headers=headers)

        # Validate the response
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        
        # Assuming the response body is in JSON format
        response_data = response.json()
    print("Response Data :" , response_data)
    end_time = time.time()
    diff_time = end_time - start_time

    assert response_data["is_enable_wallet"] is True, "Wallet should be enabled"
    assert response_data["is_enable_deposit"] is True, "deposit should be enabled"
    assert response_data["is_enable_withdraw"] is True, "withdraw should be enabled"
    assert response_data["is_enable_red_packet"] is True, "red packet should be enabled"
    assert response_data["fee_of_deposit"] == 0.0, "Unexpected deposit fee"
    assert response_data["fee_of_withdraw"] == 0.0, "Unexpected withdraw fee"
    assert response_data["min_quota_of_withdraw"] == 10.0, "Unexpected min quota of withdraw"
    assert response_data["min_quota_of_send_red_packet"] == 0.01, "Unexpected min quota for sending red packet"
    assert response_data["max_quota_of_send_red_packet"] == 50.0, "Unexpected max quota for sending red packete"


    #testing loading time
    if diff_time < 0:
        print("Test passed. ")
    else:
        send_email(subject, body, sender, recipients, password)
    assert diff_time > 5, f"too slow {diff_time}"

# Send Email
current_time = datetime.now()
formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
subject = f"Test failed  {formatted_time}"
body = "wallet config test failed please fix it."
sender = "frandyfancy@gmail.com"
recipients = "genman@twim.cc"
password = "xjbtujjvqkywrslh"

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


if __name__ == "__main__":

    pytest.main([__file__])







