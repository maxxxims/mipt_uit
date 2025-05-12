from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from collections import defaultdict
from callbacks import TopLevelCallback, SecondLevelCallback, BackButtonCallback, AnotherQuestionCallback, \
                      ThirdLevelCallback, FeedBackCallback
import pandas as pd
import emoji
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton


TEXT_BEFORE_LINK = 'Ссылка по вашему запросу:\n'


class KBTemplate():
    adjust = 1
    sep = ';'
    na_values='None'
    def __init__(self) -> None:
        self.make_kb()

    def reload(self):
        self.make_kb()


def get_button_text(row: pd.Series):
    text_emoji = ''
    if pd.notna(row['emoji']):
        text_emoji = emoji.emojize(row['emoji']) + ' '
    return text_emoji + row['name']


def add_back_button(top_kb_index: int = -1) -> InlineKeyboardButton:
    if top_kb_index < 0:
        level = 'top'
    else:
        level = 'second'
    return InlineKeyboardButton(text=emoji.emojize(":BACK_arrow:")+"Назад",
               callback_data=BackButtonCallback(top_kb_index=top_kb_index, level=level).pack())


def reload():
    ...
    
    
def get_formatted_description(selection: pd.DataFrame):
    link = selection['link'].values[0]
    name = selection['name'].values[0]
    smile = selection['emoji'].values[0]
    if pd.notna(link): 
        return TEXT_BEFORE_LINK  + f'{emoji.emojize(smile)} <a href="{link}">{name}</a> \n'
    
    description = selection['description'].values[0]
    title = emoji.emojize(smile) + f" <b>{name}</b>\n\n"
    return title + description


def get_feedback_button() -> InlineKeyboardButton: 
    return InlineKeyboardButton(text=emoji.emojize(":SOS:")+ "Сообщение в поддержку",
               callback_data=FeedBackCallback().pack())