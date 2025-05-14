import logging.config
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
import logging
from sanic import Sanic
from config import MESSAGE_AFTER_USER_TEXT
import datetime
from pytz import timezone 


async def send_email(app: Sanic, text: str, user_email: str) -> bool:
    sender = app.ctx.__getattribute__('email_login') 
    to = app.ctx.__getattribute__('email_support') 

    full_text = preprocess_text(text, user_email)

    subject="Обращение в техподдержку из телеграм бота"
    text_subtype = 'plain'
    msg = MIMEText(full_text, text_subtype)
    msg['Subject'] = subject
    msg['From'] = sender

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