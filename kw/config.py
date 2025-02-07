from dotenv import load_dotenv
import os


LINK_TO_YANDEX_SPELLER = 'http://speller.yandex.net/services/spellservice.json/checkText'
DEFAULT_PORT = 7000
DEFAULT_HOST = '0.0.0.0'
DEFAULT_SECRET = 'KEEP_IT_SECRET_KEEP_IT_SAFE'

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