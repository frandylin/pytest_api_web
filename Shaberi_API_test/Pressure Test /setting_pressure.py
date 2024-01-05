import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import csv
import uuid


def generate_device_id():
    # 生成 UUID
    device_id = uuid.uuid4()
    # 將 UUID 轉換為無連字符的16進位字串
    hex_string = str(device_id).replace('-', '')
    return hex_string[:32]

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
