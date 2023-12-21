import smtplib
from email.mime.text import MIMEText
from datetime import datetime

body = "wallet config test failed please fix it."
sender = "frandyfancy@gmail.com"
recipients = "genman@twim.cc"
password = "xjbtujjvqkywrslh"

def send_email(subject, body, sender, recipients, password):
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    subject = f"Test failed  {formatted_time}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")
