# from email.utils import parseaddr
import re

ANOTHER_QUESTION_INDEX = 'another_question'
pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


with open('data/help_service_msg.txt', 'r', encoding='utf-8') as f:
    HELP_SERVICE_MSG = f.read()


def another_question():
    return HELP_SERVICE_MSG


def validate_email(email: str) -> bool:
    if re.match(pattern, email) is not None:
        return True
    return False