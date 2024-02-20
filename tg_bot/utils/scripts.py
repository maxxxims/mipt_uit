ANOTHER_QUESTION_INDEX = 'another_question'


with open('data/help_service_msg.txt', 'r', encoding='utf-8') as f:
    HELP_SERVICE_MSG = f.read()


def another_question():
    return HELP_SERVICE_MSG