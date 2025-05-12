from dotenv import load_dotenv
import os


LINK_TO_YANDEX_SPELLER = 'http://speller.yandex.net/services/spellservice.json/checkText'
DEFAULT_PORT = 7000
DEFAULT_HOST = '0.0.0.0'
DEFAULT_SECRET = 'KEEP_IT_SECRET_KEEP_IT_SAFE'

MESSAGE_AFTER_USER_TEXT = """

Почта для обратной связи: {user_email}

================================================

ДАННОЕ СООБЩЕНИЕ АВТОМАТИЧЕСКИ СГЕНЕРИРОВАННО ПО ЗАПРОСУ ПОЛЬЗОВАТЕЛЯ. НЕ НУЖНО ОТВЕЧАТЬ НА ЭТО СООБЩЕНИЕ, ОТПРАВЬТЕ ОТВЕТ НА ПОЧТУ ПОЛЬЗОВАТЕЛЯ: {user_email}

================================================
"""

load_dotenv()

def load_backend_host():
    load_dotenv()
    return os.getenv('BACKEND_HOST', DEFAULT_HOST)

    

def load_db_url():
    load_dotenv()
    return os.getenv('DB_URL')


def load_backend_port():
    load_dotenv()
    return int(os.getenv('BACKEND_PORT', DEFAULT_PORT))


def load_private_key():
    load_dotenv()
    return os.getenv('PRIVATE_KEY', DEFAULT_SECRET)



def load_smtp_server():
    return os.getenv('SMTP_SERVER')

def load_smtp_port():
    return os.getenv('SMTP_PORT')

def load_email_login():
    
    return os.getenv('EMAIL_LOGIN')

def load_email_password():
    return os.getenv('EMAIL_PASSWORD')

def load_email_support_login():
    return os.getenv('EMAIL_SUPPORT')