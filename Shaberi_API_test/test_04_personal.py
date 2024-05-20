import requests
import pytest
import time
import os
import random
from setting import send_email, ReadCSV, Enviroment, send_signal_message

#get variable
def get_variable():
    reader_csv = ReadCSV()
    reader_csv.read_csv()
    global global_token, global_user_id
    global_token = reader_csv.token
    global_user_id = reader_csv.user_id 
global_token = None
global_user_id = None
global_random_number = None
 
get_environment_url = Enviroment().get_base_url()
env = Enviroment().env

@pytest.mark.run(order=22)
def test_revise_displayname():

    # API details
    get_variable()
    
    url = f"{get_environment_url}/_matrix/client/r0/profile/{global_user_id}/displayname"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
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
        # send_email(f"[{env}][Personal]", "revise displayname test failed please fix it.")
        send_signal_message(f"[{env}][Personal]\nrevise displayname test failed please fix it.")
    else:
        print("send message test passed. ")

    # Validate the response
    assert diff_time < 10, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

@pytest.mark.run(order=23)
def test_change_avatar():
    image_folder = os.path.join(os.path.dirname(__file__), 'assets')
    image = os.path.join(image_folder, "pepe.jpeg")
    # API details
    get_variable()
    
    url = f"{get_environment_url}/_matrix/client/r0/profile/{global_user_id}/avatar_url"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
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

@pytest.mark.run(order=24)
def test_search_profile():

    # API details
    get_variable()
    
    url = f"{get_environment_url}/_matrix/client/r0/profile/{global_user_id}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    print("url:" , url)
    print("header:" , headers)
    start_time = time.time()
    # Make the POST requests
    response = requests.get(url, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 10 or response.status_code != 200:
        # send_email(f"[{env}][Personal]", "search profile test failed please fix it.")
        send_signal_message(f"[{env}][Personal]\nsearch profile test failed please fix it.")
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


@pytest.mark.run(order=25)
def test_friend_online_status():
    
    # API details
    get_variable()

    url = f"{get_environment_url}/_matrix/client/r0/presence/{global_user_id}/status"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    print("url:", url)
    print("header:" , headers)
    start_time = time.time()
    # Make the POST requests
    response = requests.get(url, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time

    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_signal_message(f"{env} [Room]\nsearch friend status test failed please fix it.")
    else:
        print("Loading test passed. ")

    # Validate the response
    response_data = response.json()
    print("Response Data :" , response_data)
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assuming the response body is in JSON format
    assert response_data["presence"] == "online", "Response does not contain 'presence'"
    assert "last_active_ago", "Response does not contain 'last active ago'"
    assert response_data["currently_active"] == True, "Response does not contain 'currently active'"

@pytest.mark.run(order=26)
def test_change_introduction():

    global global_random_number
    random_number = random.randint(0, 1000)
    global_random_number = random_number

    # API details
    get_variable()

    url = f"{get_environment_url}/_matrix/client/r0/profile/{global_user_id}/introduction"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    data = {
        "introduction": f"API Testing Lets gooooo{random_number}"
    }
    print("url:", url)
    print("headers:", headers)
    print("POST Data:" , data)
    start_time = time.time()
    # Make the POST requests
    response = requests.put(url, json=data, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        # send_signal_message(f"{env}[Room]\nchange test failed please fix it.")
        send_signal_message(f"[{env}][Personal]\nchange introduction test failed please fix it.")
    else:
        print("change introduction test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)

@pytest.mark.run(order=27)
def test_search_introduction():

    # API details
    get_variable()

    url = f"{get_environment_url}/_matrix/client/r0/profile/{global_user_id}/introduction"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    print("url:", url)
    print("headers:", headers)
    start_time = time.time()
    # Make the POST requests
    response = requests.get(url, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_signal_message(f"[{env}][Personal]\nsearch introduction test failed please fix it.")
    else:
        print("search introduction test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert f"API Testing Lets gooooo{global_random_number}" == response_data["introduction"], "introduction was not equal."


@pytest.mark.run(order=28)
def test_search_joined_room():

    # API details
    get_variable()

    url = f"{get_environment_url}/_matrix/client/r0/joined_rooms"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    print("url:" , url)
    print("header:" , headers)
    start_time = time.time()
    # Make the POST requests
    response = requests.get(url, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_signal_message(f"[{env}][Personal]\nsearch joined room test failed please fix it.")
    else:
        print("search joined room test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert "joined_rooms" in response_data, "Response does not contain 'joined_rooms'"
    friend_room_id = response_data["joined_rooms"][0]

    # through search room members to get friend user_id
    url = f"{get_environment_url}/_matrix/client/r0/rooms/{friend_room_id}/joined_members"
    response = requests.get(url, headers=headers)
    response_data = response.json()
    print("Friend room members:" , response_data)
    global global_friend_user_id
    #get joined 字典的第一个键
    global_friend_user_id = list(response_data.get("joined", {}).keys())[0]
    print("Friend user_id:" , global_friend_user_id)
    

@pytest.mark.run(order=29)
def test_revise_friend_mark():
    #透過 joined room 中找到 room id , 再透過 search room member 得到 friend user id
    # API details
    get_variable()

    url = f"{get_environment_url}/_matrix/client/r0/user/{global_user_id}/account_data/m.remark_user_list"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    data = {
        "remark_users": {
            f"{global_friend_user_id}":f"Frandy API Test{global_random_number}"
        }
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
    if diff_time > 5 or response.status_code != 200:
        send_signal_message(f"[{env}][Personal]\nrevise friend mark test failed please fix it.")
    else:
        print("revise friend mark test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"


@pytest.mark.run(order=30)
def test_search_friend_mark():
    # API details
    get_variable()

    url = f"{get_environment_url}/_matrix/client/r0/user/{global_user_id}/account_data/m.remark_user_list"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    print("url:" , url)
    print("header:" , headers)
    start_time = time.time()
    # Make the POST requests
    response = requests.get(url, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        send_signal_message(f"[{env}][Personal]\nsearch friend mark test failed please fix it.")
    else:
        print("search friend mark test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)
    assert response_data.get("remark_users", {}).get(f"{global_friend_user_id}") == f"Frandy API Test{global_random_number}", "friend mark was not equal."

@pytest.mark.run(order=31)
def test_logout():

    #API details
    get_variable()
    
    url = f"{get_environment_url}/_matrix/client/r0/logout"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    print("url:" , url)
    print("header:" , headers)
    start_time = time.time()
    # Make the POST requests
    response = requests.post(url, headers=headers)
    end_time = time.time()
    diff_time = end_time - start_time
    #testing loading time
    if diff_time > 5 or response.status_code != 200:
        # send_signal_message(f"{env}[Room]\nsend red packet test failed please fix it.")
        send_signal_message(f"[{env}][Personal]\nlogout test failed please fix it.")
    else:
        print("send message test passed. ")

    # Validate the response
    assert diff_time < 5, f"too slow {diff_time}"
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    # Assuming the response body is in JSON format
    response_data = response.json()
    print("Response Data :" , response_data)


if __name__ == "__main__":


    pytest.main([__file__])







