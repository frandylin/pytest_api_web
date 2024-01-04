import requests
import json
import uuid
import time
import hashlib

host_domain = "https://im-dev.imdevs.net/"

token_table = {}
room_id = "!285158562400:shaberi.com"
for i in range(1, 200):
    # 請求驗證碼
    phone_number = f"910100{i:03d}"
    print(f"[{phone_number}] 驗證碼")
    url = f"{host_domain}_matrix/client/r0/register/msisdn/requestCode"
    client_secret = uuid.uuid4().hex
    payload = json.dumps(
        {
            "country": "TW",
            "phone_number": phone_number,
            "client_secret": client_secret,
            "send_attempt": 1,
            "msisdn_use": "login",
        }
    )
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    session_id = json.loads(response.text)["sid"]
    time.sleep(5)
    # 登入
    print(f"[{phone_number}] 登入")
    url = f"{host_domain}_matrix/client/r0/login/msisdnlogin"
    payload = json.dumps(
        {
            "session_id": session_id,
            "client_secret": client_secret,
            "code": "888888",
            "device_id": f"web_[postman]{client_secret}",
            "initial_device_display_name": f"{phone_number}",
        }
    )
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload)
    res_json = json.loads(response.text)
    user_id = res_json["user_id"]
    access_token = res_json["access_token"]
    token_table[phone_number] = (user_id, access_token)
    time.sleep(5)
    print(f"[{phone_number}] 改暱稱")
    # 改暱稱
    url = f"{host_domain}_matrix/client/r0/profile/{user_id}/displayname"
    payload = json.dumps({"displayname": f"{phone_number}"})
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    # sync
    print(f"[{phone_number}] sync")
    url = f"{host_domain}_matrix/client/r0/sync?timeout=0"
    payload = {}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # createRoom
    # url = f"{host_domain}_matrix/client/r0/createRoom"
    # payload = json.dumps(
    #     {
    #         "name": "紅包測試群",
    #         "preset": "public_chat",
    #         "visibility": "public",
    #         "initial_state": [
    #             # {
    #             #     "type": "m.room.encryption",
    #             #     "state_key": "",
    #             #     "content": {"algorithm": "m.megolm.v1.aes-sha2"},
    #             # },
    #         ],
    #     }
    # )
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer syt_bnc1NXp0bnBrczBt_XoxTgSZUEuYtlXiwwADX_0MrdSE",
    # }
    # response = requests.request("POST", url, headers=headers, data=payload)
    # res_json = json.loads(response.text)
    # room_id = res_json["room_id"]
    # join room
    time.sleep(5)
    print(f"[{phone_number}] join room")
    url = f"{host_domain}_matrix/client/r0/join/{room_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"[{phone_number}] 打個字")
    url = f"{host_domain}_matrix/client/r0/rooms/{room_id}/send/m.room.message/m{int(time.time())}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = json.dumps({"msgtype": "m.text", "body": f"[報數] {phone_number}"})
    response = requests.request("PUT", url, headers=headers, data=payload)


for phone_number in sorted(token_table.keys()):
    user_id, access_token = token_table[phone_number]
    print(f"[{phone_number}] 打個字")
    url = f"{host_domain}_matrix/client/r0/rooms/{room_id}/send/m.room.message/m{int(time.time())}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = json.dumps({"msgtype": "m.text", "body": f"[報數] {phone_number}"})
    response = requests.request("PUT", url, headers=headers, data=payload)

# 啟用錢包
for phone_number in sorted(token_table.keys()):
    user_id, access_token = token_table[phone_number]
    url = f"{host_domain}_matrix/client/r0/wallet/{user_id}/pay_password"
    user_id, access_token = token_table[phone_number]
    input_string = f"{user_id}:135790"
    md5 = hashlib.md5()
    md5.update(input_string.encode("utf-8"))
    md5_hash = md5.hexdigest()
    payload = json.dumps({"wallet_password": f"{md5_hash}"})
    print(f"{user_id} {md5_hash}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.request("POST", url, headers=headers, data=payload)


# 發紅包
def send_red_packet():
    phone_number = "910100001"
    user_id, access_token = token_table[phone_number]
    url = f"{host_domain}_matrix/client/r0/wallet/{user_id}/rooms/{room_id}/red_packet"
    user_password = f"{user_id}:135790"
    md5 = hashlib.md5()
    md5.update(user_password.encode("utf-8"))
    md5_password = md5.hexdigest()
    key = "shaberi_key_2023"
    red_packet_type = 10
    total_amount = "10.000"
    fee = "0.000"
    count = 200
    sign_str = f"{md5_password}:{user_id}:{total_amount}:{fee}:{count}:{red_packet_type}:{room_id}:{key}"
    md5 = hashlib.md5()
    md5.update(sign_str.encode("utf-8"))
    sign = md5.hexdigest()
    payload = json.dumps(
        {
            "red_packet_type": red_packet_type,
            "count": count,
            "total_amount": total_amount,
            "note": "恭喜發財",
            "sign": sign,
            "fee": fee,
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res_json = json.loads(response.text)
    red_packet_id = res_json["red_packet_id"]
    expire_at = res_json["expire_at"]
    print(response.text)
    url = f"{host_domain}_matrix/client/r0/rooms/{room_id}/send/m.red_packet.send/m{int(time.time())}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = json.dumps(
        {
            "body": "恭喜發財!",
            "count": count,
            "expire_at": expire_at,
            "fee": fee,
            "msgtype": "m.red_packet",
            "red_packet_id": red_packet_id,
            "red_packet_type": red_packet_type,
            "total_amount": total_amount,
            "tran_amount": total_amount,
        }
    )
    response = requests.request("PUT", url, headers=headers, data=payload)
    return red_packet_id


red_packet_id = send_red_packet()
##### 發紅包 結束 #####

#### 領紅包 開始###
for phone_number in sorted(token_table.keys()):
    user_id, access_token = token_table[phone_number]
    url = f"{host_domain}_matrix/client/r0/wallet/{user_id}/rooms/{room_id}/red_packet/{red_packet_id}/claim"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    res_json = json.loads(response.text)
    if "remain" not in res_json:
        continue
    remain = res_json["remain"]
    tran_amount = res_json["tran_amount"]
    url = f"{host_domain}_matrix/client/r0/rooms/{room_id}/send/m.red_packet.claim/m{int(time.time())}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = json.dumps(
        {
            "msgtype": "m.red_packet",
            "red_packet_id": red_packet_id,
            "red_packet_sender_id": user_id,
            "remain": f"{remain}",
            "tran_amount": f"{tran_amount}",
        }
    )
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(f"[{phone_number}] 領紅包訊息")


with open("dev_user.json", "w") as outfile:
    outfile.write(json.dumps(token_table))
