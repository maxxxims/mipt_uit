import logging.config
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import logging
from sanic import Sanic
from config import MESSAGE_AFTER_USER_TEXT
import datetime
from pytz import timezone 
import base64

async def send_email(app: Sanic, text: str, user_email: str, attachments: list = None) -> bool:
    sender = app.ctx.__getattribute__('email_login') 
    to = app.ctx.__getattribute__('email_support') 

    print('HERE IN UTILS')
    full_text = preprocess_text(text, user_email)

    subject="Обращение в техподдержку из телеграм бота"
    msg = MIMEMultipart() 
    msg.attach(MIMEText(full_text, 'plain', 'utf-8'))
    msg['Subject'] = subject
    msg['From'] = sender

    print('HERE!!!! IN UTILS')

    if attachments:
        for file_type, filename, file_data in attachments:
            file_data = bytes.fromhex(file_data)
            part = MIMEApplication(file_data, Name=filename)
            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            msg.attach(part)

    try:
        async with app.ctx.__getattribute__('SMTP') as smtp:
            await smtp.send_message(msg, sender=sender, recipients=to)
        return True
    except Exception as e:
        print(e)
        logging.error(f'Error: {e}')
        return False
    

def preprocess_text(text: str, user_email):
    date = datetime.datetime.now(timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
    return text + '\n' + MESSAGE_AFTER_USER_TEXT.format(user_email=user_email, date=date)