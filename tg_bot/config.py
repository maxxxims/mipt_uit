from dotenv import load_dotenv
import os
from aiogram.types import FSInputFile


DEFAULT_TEXT = 'Выберите необходимый пункт'
GREETING_TEXT = "Выберите нужный пункт в меню."

START_GREETING_TEXT = "Здравствуйте! \nЯ Анжела. Чат-бот технической поддержки УИТ. \nЧем могу помочь? Выберите нужный пункт в меню.\nНе нашли? Введите запрос."

GREETING_IMAGE = FSInputFile("data/greeting_image.jpg")

MSG_AFTER_FIND_TOPICS = "Вот, что я нашла по вашему запросу:"
MSG_AFTER_NOT_FOUND = "Нужный сервис не найден, вы можете воспользоваться контактами техподдержки УИТ: helpdesk@mipt.ru, redmine.mipt.ru"

MSG_ANOTHER_QUESTION = """Если вы не нашли нужный сервис, вы можете отправить запрос мне или воспользоваться контактами техподдержки УИТ: 
helpdesk@mipt.ru 
redmine.mipt.ru
"""


def load_token():
    load_dotenv()
    return os.getenv("TOKEN")

def load_backend_url():
    load_dotenv()
    return os.getenv("BACKEND_URL")


def load_sticker_id():
    load_dotenv()
    return os.getenv("STICKER_ID")