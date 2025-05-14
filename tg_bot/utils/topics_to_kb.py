from keyboards import second_level_kb, third_level_kb, main_kb
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from callbacks import CloseRecommendationKBCallback, NothingFindingCallback



def get_first_kb(t: dict) -> InlineKeyboardButton:
    top_kb_index = t['top_kb_index']
    # kb_list = main_kb.kb_array
    # btn = kb_list[top_kb_index - 1][0]
    btn = main_kb.kb_mapping[top_kb_index][0]
    return btn


def get_second_kb(t: dict) -> InlineKeyboardButton:
    top_kb_index = t['top_kb_index']
    second_kb_index = t['second_kb_index']
    #kb_list = second_level_kb.keyboards_list[top_kb_index - 1]
    kb_list = second_level_kb.index_to_keyboard[top_kb_index]
    btn = kb_list[second_kb_index - 1][0]
    return btn


def get_third_kb(t: dict) -> InlineKeyboardButton:
    top_kb_index = t['top_kb_index']
    second_kb_index = t['second_kb_index']
    third_kb_index = t['third_kb_index']
    kb_list = third_level_kb.get_kb(top_kb_index, second_kb_index)

    btn = kb_list[third_kb_index - 1]
    btn2 = btn[0]
    return btn2


import logging

logging.basicConfig(level=logging.INFO)

def get_kb_from_topics(topics: list) -> InlineKeyboardMarkup:
    kb_list = []
    logging.info(f"TOPICS:::")
    for topic in topics:
        logging.info((topic['top_kb_index'], topic['second_kb_index'], topic['third_kb_index'], topic['name']))
        if topic['second_kb_index'] < 0:
            try:
                button = get_first_kb(topic)
            except Exception as e:
                logging.error(e)
                button = None
            
        elif topic['third_kb_index'] < 0:
            try:
                button = get_second_kb(topic)
            except Exception as e:
                logging.error(e)
                button = None
        elif topic['third_kb_index'] > 0:
            try:
                button = get_third_kb(topic)
            except Exception as e:
                logging.error(e)
                button = None
        if button is not None:
            kb_list.append([button])


    kb_list.append([InlineKeyboardButton(text='🆘 Нужный сервис не найден', callback_data=NothingFindingCallback().pack())])
    #kb_list.append([InlineKeyboardButton(text='❌ Закрыть', callback_data=CloseRecommendationKBCallback().pack()),])
    #✖️
    return InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )