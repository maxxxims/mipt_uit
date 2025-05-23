from dotenv import load_dotenv
import os
from aiogram.types import FSInputFile


DEFAULT_TEXT = 'Выберите необходимый пункт'
GREETING_TEXT = "Выберите нужный пункт в меню."

START_GREETING_TEXT = "Здравствуйте! \nЯ Анжела. Чат-бот технической поддержки УИТ. \nЧем могу помочь? Выберите нужный пункт в меню.\nНе нашли? Введите запрос."

GREETING_IMAGE = FSInputFile("data/greeting_image.jpg")

MSG_AFTER_FIND_TOPICS = "Вот, что я нашла по вашему запросу:"
MSG_AFTER_NOT_FOUND = "Нужный сервис не найден, вы можете воспользоваться контактами техподдержки УИТ: helpdesk@mipt.ru, redmine.mipt.ru \nВы можете отправить обращение в техподдержку, для этого нажмите на кнопку ниже:"

# MSG_FOR_FEEDBACK_ABILITY = """Вы можете в"""

MSG_ANOTHER_QUESTION = """Если вы не нашли нужный сервис, вы можете отправить запрос мне или воспользоваться контактами техподдержки УИТ: 
helpdesk@mipt.ru 
redmine.mipt.ru
"""

DEFAULT_SECRET = 'KEEP_IT_SECRET_KEEP_IT_SAFE'

# FEEDBACK_MSG_1 = """Чтобы отправить отзыв, введите команду /feedback и напишите ваш отзыв:"""
# FEEDBACK_MSG_2 = """Отправьте почту, на которую необходимо будет отправить ответ от техподдержки"""
# FEEDBACK_MSG_3 = """Ваш запрос передан в техподдержку!"""
# FEEDBACK_MSG_END = """Вы прекратили заполнение формы"""


FEEDBACK_MSG_1 = """Напишите почту, на которую нужно будет отправить ответ. Если вы передумали, нажмите на кнопку ниже: """
FEEDBACK_MSG_2 = """Напишите запрос к техподдержке в одном сообщении. Если вы передумали, нажмите на кнопку ниже: """
FEEDBACK_MSG_3 = """Ваш запрос передан в техподдержку!"""
FEEDBACK_MSG_END = """Вы прекратили заполнение формы"""


def load_token():
    load_dotenv()
    return os.getenv("TOKEN")

def load_backend_url():
    load_dotenv()
    return os.getenv("BACKEND_URL")


def load_sticker_id():
    load_dotenv()
    return os.getenv("STICKER_ID")

    
def load_private_key():
    load_dotenv()
    return os.getenv('PRIVATE_KEY', DEFAULT_SECRET)