import requests
import pytest
import time
import hashlib
from setting import send_email, ReadCSV, send_shaberi_message, Enviroment, send_signal_message

#get variable
def get_variable():
    reader_csv = ReadCSV()
    reader_csv.read_csv()
    global global_token, global_user_id, global_wallet_password
    global_token = reader_csv.token
    global_user_id = reader_csv.user_id 
    global_wallet_password = reader_csv.wallet_password
global_token = None
global_user_id = None 
global_wallet_password = None
global_room_id = None
global_red_packet_id = None

get_environment_url = Enviroment().get_base_url()
env = Enviroment().env
current_time = int(time.time())

@pytest.mark.run(order=12)
def test_create_room():
    
    # API details
    get_variable()
    url = f"{get_environment_url}/_matrix/client/r0/createRoom"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
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
        send_email(f"[{env}][Room]", "create room test failed please fix it.")
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

@pytest.mark.run(order=13)
def test_send_packet():
    if env == "prod":
        pytest.skip("Test skipped because environment is not uat or stg")

    # API details
    get_variable()
    url = f"{get_environment_url}/_matrix/client/r0/wallet/{global_user_id}/rooms/{global_room_id}/red_packet"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    total_amount = "0.010"
    count = 1
    fee = "0.000"
    red_packet_type = 10
    key = "shaberi_key_2023"
    
    print(f"{global_wallet_password}:{global_user_id}:{total_amount}:{fee}:{count}:{red_packet_type}:{global_room_id}:{key}")
    data_hash = f"{global_wallet_password}:{global_user_id}:{total_amount}:{fee}:{count}:{red_packet_type}:{global_room_id}:{key}".encode('utf-8')
    wallet_sign = hashlib.md5(data_hash).hexdigest()
    data = {
        #1 是單人 10 群組隨機 11群組固定
        "red_packet_type": red_packet_type, 
        "count": count,
        "total_amount": total_amount,
        "note": "恭喜發財 😂",
        "sign":f"{wallet_sign}",
        "fee": fee,
        "version":2
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(2):
        # Make the POST requests
        response = requests.post(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time

    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_signal_message(f"{env}[Room]\nsend red packet test failed please fix it.")
    else:
        print("Loading test passed. ")

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

@pytest.mark.run(order=14)
def test_receive_packet():
    if env == "prod":
        pytest.skip("Test skipped because environment is not uat or stg")

    # API details
    get_variable()
    url = f"{get_environment_url}/_matrix/client/r0/wallet/{global_user_id}/rooms/{global_room_id}/red_packet/{global_red_packet_id}/claim"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}

    data = {

    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    start_time = time.time()
    for i in range(2):
        # Make the POST requests
        response = requests.post(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time

    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_signal_message(f"{env} [Room]\nreceive red packet test failed please fix it.")
    else:
        print("Loading test passed. ")
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
    

@pytest.mark.run(order=15)
def test_send_message():

    # API details
    get_variable()
    url = f"{get_environment_url}/_matrix/client/r0/rooms/{global_room_id}/send/m.room.message/m{current_time}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    data = {
        "msgtype": "m.text",
        "body": "frandy"
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
    if diff_time > 10 or response.status_code != 200:
        send_email(f"[{env}][Message]", "send message test failed please fix it.")
    else:
        print("send message test passed. ")

    # Validate the response
    assert diff_time < 10, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "$" in response_data["event_id"], "Response does not contain 'event_id'"

@pytest.mark.run(order=16)
def test_revise_room_name():

    # API details
    get_variable()
    url = f"{get_environment_url}/_matrix/client/r0/rooms/{global_room_id}/state/m.room.name/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    data = {
        "name": "frandy api test"
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    # Make the POST requests
    response = requests.put(url, json=data, headers=headers)
    
    # Validate the response
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "$" in response_data["event_id"], "Response does not contain 'event_id'"

@pytest.mark.run(order=17)
def test_serch_room_members():

    # API details
    get_variable()
    url = f"{get_environment_url}/_matrix/client/r0/rooms/{global_room_id}/joined_members"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    data = {
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    # Make the POST requests
    response = requests.get(url, json=data, headers=headers)
    
    # Validate the response
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "joined" in response_data, "Response does not contain 'event_id'"

@pytest.mark.run(order=18)
def test_leave_room():

    # API details
    get_variable()
    url = f"{get_environment_url}/_matrix/client/r0/rooms/{global_room_id}/leave"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
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
        send_email(f"[{env}][Room]", "leave room test failed please fix it.")
    else:
        print("Loading test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)


@pytest.mark.run(order=19)
def test_announce_message():

    # API details
    get_variable()
    url = f"{get_environment_url}/_matrix/client/r0/system/board?update_ts={current_time}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    data = {
    }
    print("url:" , url)
    print("header:" , headers)
    start_time = time.time()
    for i in range(5):
        # Make the POST requests
        response = requests.get(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_signal_message(f"{env} [Room]\nannounce message test failed please fix it.")
    else:
        print("Loading test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "event_id" in response_data["events"][0], "Response does not contain 'event_id"
    assert "content" in response_data["events"][0], "Response does not contain 'content"
    assert "origin_server_ts" in response_data["events"][0], "Response does not contain 'origin_server_ts"
    assert "type" in response_data["events"][0], "Response does not contain'type"
    assert "sender" in response_data["events"][0], "Response does not contain'sender"
    assert "is_show" in response_data["events"][0], "Response does not contain'is_show"

if __name__ == "__main__":


    pytest.main([__file__])







