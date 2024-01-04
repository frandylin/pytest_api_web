import requests
import json
import uuid
import time
import hashlib
from setting_pressure import get_environment_url, generate_device_id
import uuid
import random

token_table = {}
env = "stg"
room_id = "!995433889696:shaberi.com"
current_time = int(time.time())
# for i in range(1, 30):
#     #請求驗證碼
#     phone_number = f"09{random.randint(10000000, 99999999)}"
#     print(f"[{phone_number}] 驗證碼")
#     secret = str(uuid.uuid4())
#     url = f"{get_environment_url(env)}/_matrix/client/r0/register/msisdn/requestCode"
#     headers = {"Content-Type": "application/json"}
#     data = {
#         "country": "TW",
#         "phone_number": phone_number,
#         "client_secret": secret,
#         "send_attempt": 1,
#         "msisdn_use": "login"
#     }
#     response = requests.post(url, json=data, headers=headers)
#     response_data = response.json()
#     sid = response_data.get("sid")
#     time.sleep(5)
#     #登入
#     print(f"[{phone_number}] 登入")
#     url = f"{get_environment_url(env)}/_matrix/client/r0/login/msisdnlogin"
#     headers = {"Content-Type": "application/json"}
#     device_id = generate_device_id()
#     data = {
#         "session_id": sid,
#         "client_secret": secret,
#         "code": "888888",
#         "device_id": f"{device_id}",
#         "initial_device_display_name": f"{phone_number}"
#     }
#     response = requests.post(url, json=data, headers=headers)
#     response_data = response.json()
#     token = response_data.get("access_token")
#     user_id = response_data.get("user_id")
#     token_table[phone_number] = (user_id, token)
#     time.sleep(5)
#     print(f"[{phone_number}] 改暱稱")
#     #改暱稱
#     url = f"{get_environment_url(env)}/_matrix/client/r0/profile/{user_id}/displayname"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
#     data = {
#         "displayname": f"frandy robot {random.randint(1, 9999)}",
#     }
#     response = requests.put(url, json=data, headers=headers)
#     #sync
#     print(f"[{phone_number}] sync")
#     url = f"{get_environment_url(env)}/_matrix/client/r0/sync?filter=1&timeout=0&full_state=true"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
#     data = {
#     }
#     response = requests.get(url, json=data, headers=headers)
#     time.sleep(5)
#     print(f"[{phone_number}] join room")
#     #加入房間
#     url = f"{get_environment_url(env)}/_matrix/client/r0/join/{room_id}"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
#     data = {
#     }
#     response = requests.post(url, json=data, headers=headers)
#     print(f"[{phone_number}] send message")
#     #打字
#     url = f"{get_environment_url(env)}/_matrix/client/r0/rooms/{room_id}/send/m.room.message/m{current_time}"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
#     data = {
#         "msgtype": "m.text",
#         "body": f"報數!!!{phone_number}"
#     }
#     response = requests.put(url, json=data, headers=headers)

# 读取 user.json 文件的现有数据，如果文件不存在则创建一个空字典
# try:
#     with open("user.json", "r") as infile:
#         existing_data = json.load(infile)
# except FileNotFoundError:
#     existing_data = {}
#     # 将新数据合并到现有数据中
# existing_data.update(token_table)

# with open("user.json", "w") as outfile:
#     outfile.write(json.dumps(existing_data))


token_table = {}
with open("user.json", "r") as infile:
    # 逐行读取文件
    for line in infile:
        # 将每行的 JSON 数据解析为字典
        data = json.loads(line)
        
        # 将解析的数据合并到 token_table 中
        token_table.update(data)

# for phone_number in sorted(token_table.keys()):
#     user_id, token = token_table[phone_number]
#     print(f"[{phone_number}] 打個字")
#     url = f"{get_environment_url(env)}/_matrix/client/r0/rooms/{room_id}/send/m.room.message/m{current_time}"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
#     data = {
#         "msgtype": "m.text",
#         "body": f"報數!!!{phone_number}"
#     }
#     response = requests.put(url, json=data, headers=headers)

#啟用錢包
# for phone_number in sorted(token_table.keys()):
#     user_id, token = token_table[phone_number]
#     print(f"[{phone_number}] 啟用錢包")
#     url = f"{get_environment_url(env)}/_matrix/client/r0/wallet/{user_id}/pay_password"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

#     #pre-request script
#     password = "888888"
#     data = f"{user_id}:{password}".encode('utf-8')
#     wallet_password = hashlib.md5(data).hexdigest()
#     data = {
#         "wallet_password": f"{wallet_password}"
#     }
#     response = requests.post(url, json=data, headers=headers)
#     response_data = response.json()
#     print("Response Data :" , response_data)

#發紅包
# def send_packet():
#     print("發紅包")
#     phone_number = "0909317920"
#     user_id, token = token_table[phone_number]
#     # API details
#     url = f"{get_environment_url(env)}/_matrix/client/r0/wallet/{user_id}/rooms/{room_id}/red_packet"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
#     password = "888888"
#     data = f"{user_id}:{password}".encode('utf-8')
#     wallet_password = hashlib.md5(data).hexdigest()
#     total_amount = "40.000"
#     count = 10
#     fee = "0.000"
#     red_packet_type = 10
#     key = "shaberi_key_2023"
#     print("token:", token)
#     print(f"{wallet_password}:{user_id}:{total_amount}:{fee}:{count}:{red_packet_type}:{room_id}:{key}")
#     data_hash = f"{wallet_password}:{user_id}:{total_amount}:{fee}:{count}:{red_packet_type}:{room_id}:{key}".encode('utf-8')
#     wallet_sign = hashlib.md5(data_hash).hexdigest()
#     data = {
#         #1 是單人 10 群組隨機 11群組固定
#         "red_packet_type": red_packet_type, 
#         "count": count,
#         "total_amount": total_amount,
#         "note": "恭喜發財 😂",
#         "sign":f"{wallet_sign}",
#         "fee": fee
#     }
#     print("POST Data:" , data)
#     # Make the POST requests
#     response = requests.post(url, json=data, headers=headers)

#     # Validate the response
#     response_data = response.json()
#     print("Response Data :" , response_data)
#     red_packet_id = response_data.get("red_packet_id")
#     expire_at = response_data.get("expire_at")

#     #發紅包訊息
#     print("發紅包訊息")
#     url = f"{get_environment_url(env)}/_matrix/client/r0/rooms/{room_id}/send/m.red_packet.send/m{current_time}"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
#     data = {
#         "body": "frandy 發的紅包快來搶啊!",
#         "count": count,
#         "expire_at": expire_at,
#         "fee": fee,
#         "msgtype": "m.red_packet",
#         "red_packet_id": red_packet_id,
#         "red_packet_type": red_packet_type,
#         "total_amount": total_amount,
#         "tran_amount": total_amount,
#     }
#     print("POST Data:" , data)
#     response = requests.put(url, json=data, headers=headers)
#     response_data = response.json()
#     print("Response Data :" , response_data)
#     return red_packet_id

red_packet_id = "7012b4ca-b93d-42ab-aabd-1bc81acdd1a8"

#領紅包
for phone_number in sorted(token_table.keys()):
    user_id, token = token_table[phone_number]
    print("領紅包")
    url = f"{get_environment_url(env)}/_matrix/client/r0/wallet/{user_id}/rooms/{room_id}/red_packet/{red_packet_id}/claim"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    data = {

    }
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    print("Response Data :" , response_data)
    if "remain" not in response_data:
        continue
    remain = response_data.get("remain")
    tran_amount = response_data.get("tran_amount")
    #傳送系統訊息
    print(f"[{phone_number}] 領紅包訊息")
    url = f"{get_environment_url(env)}/_matrix/client/r0/rooms/{room_id}/send/m.red_packet.claim/m{current_time}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    data = {
        "msgtype": "m.red_packet",
        "red_packet_id": red_packet_id,
        "red_packet_sender_id": user_id,
        "remain": f"{remain}",
        "tran_amount": f"{tran_amount}",
    }
    response = requests.put(url, json=data, headers=headers)
    print("Post Data :" , data)
    response_data = response.json()
    print("Response Data :" , response_data)
    print("Response Data :" , response.status_code)
    


