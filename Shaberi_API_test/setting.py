import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import csv
import uuid
import time
import requests


def generate_device_id():
    # 生成 UUID
    device_id = uuid.uuid4()
    # 將 UUID 轉換為無連字符的16進位字串
    hex_string = str(device_id).replace('-', '')
    return hex_string[:32]

#send email
body = "wallet config test failed please fix it."
sender = "frandyfancy@gmail.com"
recipients = "genman@twim.cc"
password = "xjbtujjvqkywrslh"

def send_email(subject_prefix, body, sender, recipients, password):
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    #subject_prefix 由 Login , Wallet 帶入prefix 
    subject = f"{subject_prefix} Test failed  {formatted_time}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


#env
urls = {
    "prod": "https://api.imser5yw.com",
    "uat": "https://im-uat.imdevs.net",
    "stg": "https://im-stg.imdevs.net",
    "dev": "https://im-dev.imdevs.net",
}

def get_environment_url(env):
    if env == "prod":
        return urls["prod"]
    elif env == "uat":
        return urls["uat"]
    elif env == "stg":
        return urls["stg"]
    elif env == "dev":
        return urls["dev"]

#only for wallet urls
def get_environment_wallet_url(env):
    if env == "prod":
        return "https://svzyyges3qk6b6s62v88qts.letsgomars.com"
    elif env == "uat":
        return "https://im-uat-aaj7xg4ds.imdevs.net"
    elif env == "stg":
        return "https://im-stg-pzx.imdevs.net"
    elif env == "dev":
        return "https://im-dev-pzx.imdevs.net"

class ReadCSV:
    def __init__(self):
        # 初始化类的属性
        self.token = None
        self.user_id = None
        self.sid = None
        self.client_secret = None
        self.wallet_password = None

    def read_csv(self):
        # 从 CSV 文件中读取设置并将其存储在类的属性中
        with open("token.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == "token":
                    self.token = row[1]
                elif row[0] == "user_id":
                    self.user_id = row[1]
                elif row[0] == "sid":
                    self.sid = row[1]
                elif row[0] == "client_secret":
                    self.client_secret = row[1]
                elif row[0] == "wallet_password":
                    self.wallet_password = row[1]

# global_token = "syt_djhqN3Mybjh5YWd1_FRACHIpNMzXoBGRzWsrN_0quZSK"
# message = "fuck"
def send_shaberi_message(global_token, message):
    current_time = int(time.time())
    # API details
    env = "uat"
    url = f"{get_environment_url(env)}/_matrix/client/r0/rooms/!183481292480:shaberi.com/send/m.room.message/m{current_time}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {global_token}"}
    data = {
        "msgtype": "m.text",
        "body": message
    }
    print("url:" , url)
    print("header:" , headers)
    print("POST Data:" , data)
    # Make the POST requests
    response = requests.put(url, json=data, headers=headers)
    response_data = response.json()
    print("Response Data :" , response_data)

# def read_csv():
#     token, user_id, sid, client_secret, wallet_password = None, None, None, None, None
#     with open("token.csv", "r") as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             if row[0] == "token":
#                 token = row[1]
#             elif row[0] == "user_id":
#                 user_id = row[1]
#             elif row[0] == "sid":
#                 sid = row[1]
#             elif row[0] == "client_secret":
#                 client_secret = row[1]
#     return token, user_id, sid, client_secret 