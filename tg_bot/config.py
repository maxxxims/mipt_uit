from dotenv import load_dotenv
import os
from aiogram.types import FSInputFile


DEFAULT_TEXT = 'Выберите необходимый пункт'
GREETING_TEXT = "Здравствуйте! \nЯ Анжела. Чат-бот технической поддержки УИТ. \nЧем могу помочь? Выберите нужный пункт в меню."

GREETING_IMAGE = FSInputFile("data/greeting_image.jpg")

MSG_AFTER_FIND_TOPICS = "Вот, что я нашла по Вашему запросу:"
MSG_AFTER_NOT_FOUND = "Нужный сервис не найден, вы можете воспользоваться контактами техподдержки УИТ: helpdesk@mipt.ru, redmine.mipt.ru"

MSG_ANOTHER_QUESTION = "Введите запрос"

is_prod = True

def load_token():
    load_dotenv()
    return os.getenv("TOKEN")

def load_backend_url(prod=is_prod):
    load_dotenv()
    if prod:
        return os.getenv("BACKEND_URL_PROD")
    else:
        return os.getenv("BACKEND_URL_TEST")


def load_sticker_id():
    load_dotenv()
    return os.getenv("STICKER_ID")