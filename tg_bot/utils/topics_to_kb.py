from keyboards import second_level_kb, third_level_kb
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from callbacks import CloseRecommendationKBCallback, NothingFindingCallback


def get_second_kb(t: dict) -> InlineKeyboardButton:
    top_kb_index = t['top_kb_index']
    second_kb_index = t['second_kb_index']
    kb_list = second_level_kb.keyboards_list[top_kb_index - 1]
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



def get_kb_from_topics(topics: list) -> InlineKeyboardMarkup:
    kb_list = []
    for topic in topics:
        if topic['third_kb_index'] < 0:
            button = get_second_kb(topic)
            kb_list.append([button])
        else:
            button = get_third_kb(topic)
            kb_list.append([button])


    kb_list.append([InlineKeyboardButton(text='🆘 Нужный сервис не найден', callback_data=NothingFindingCallback().pack())])
    #kb_list.append([InlineKeyboardButton(text='❌ Закрыть', callback_data=CloseRecommendationKBCallback().pack()),])
    #✖️
    return InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )