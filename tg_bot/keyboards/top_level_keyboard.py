from .keyboard import KBTemplate, get_button_text
import pandas as pd
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from callbacks import *


class MainKB(KBTemplate):
    path_to_csv = "data/kb_top_level.csv"
    def make_kb(self):
        data = pd.read_csv(self.path_to_csv, sep=self.sep, na_values=self.na_values)
        self.kb_array = []

        for i, row in data.iterrows():
            button_text = get_button_text(row)
            if row['top_kb_index'] < 0:
                self.kb_array.append([InlineKeyboardButton(text=button_text, 
                               callback_data=AnotherQuestionCallback().pack())])
            else:
                self.kb_array.append([InlineKeyboardButton(text=button_text, 
                               callback_data=TopLevelCallback(top_kb_index=row['top_kb_index']).pack())])

        self.kb = InlineKeyboardMarkup(
            inline_keyboard=self.kb_array
        )


main_kb = MainKB()


def get_main_kb() -> InlineKeyboardMarkup:
    return main_kb.kb