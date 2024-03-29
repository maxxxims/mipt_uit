from dotenv import load_dotenv
import os


LINK_TO_YANDEX_SPELLER = 'http://speller.yandex.net/services/spellservice.json/checkText'


def load_backend_host():
    load_dotenv()
    return os.getenv('BACKEND_HOST')

    

def load_db_url():
    load_dotenv()
    return os.getenv('DB_URL')


def load_backend_port():
    load_dotenv()
    return int(os.getenv('BACKEND_PORT'))
