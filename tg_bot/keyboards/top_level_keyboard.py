from .keyboard import TEXT_BEFORE_LINK, KBTemplate, get_button_text, get_formatted_description, get_feedback_button
import pandas as pd
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from callbacks import *


class MainKB(KBTemplate):
    path_to_csv = "data/kb_top_level.csv"
    def make_kb(self):
        self.data = pd.read_csv(self.path_to_csv, sep=self.sep, na_values=self.na_values)
        self.kb_array = []
        # print(self.data)
        for i, row in self.data.iterrows():
            # print(row)
            button_text = get_button_text(row)
            if row['top_kb_index'] < 0:
                self.kb_array.append([InlineKeyboardButton(text=button_text, 
                               callback_data=AnotherQuestionCallback().pack())])
            elif pd.notna(row['link']):
                print('NOT NULL!!!!!!!!!!!!!!!!!!!!!!!!')
                self.kb_array.append([InlineKeyboardButton(text=button_text,
                                    callback_data=TopLevelCallback(top_kb_index=row['top_kb_index'], next_kb=False).pack())])

            else:
                self.kb_array.append([InlineKeyboardButton(text=button_text, 
                               callback_data=TopLevelCallback(top_kb_index=row['top_kb_index']).pack())])

        self.kb_array.append([get_feedback_button()])
        self.kb = InlineKeyboardMarkup(
            inline_keyboard=self.kb_array
        )


main_kb = MainKB()


def get_main_kb() -> InlineKeyboardMarkup:
    return main_kb.kb


def get_link_from_top_kb(top_kb_index: int) -> str:
    df = main_kb.data
    selection = df.loc[(df['top_kb_index'] == top_kb_index)]
    return get_formatted_description(selection)