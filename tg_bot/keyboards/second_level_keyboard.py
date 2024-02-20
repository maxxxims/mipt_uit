from .keyboard import KBTemplate, get_button_text, add_back_button, TEXT_BEFORE_LINK
import pandas as pd
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from callbacks import *


class SecondLevelKB(KBTemplate):
    path_to_csv = "data/kb_second_level_oldmipt.csv"
    def make_kb(self, back_button: bool = True) -> None:
        self.data = pd.read_csv(self.path_to_csv, sep=self.sep, na_values=self.na_values)
        keyboards_number = len(self.data['top_kb_index'].unique())
        self.keyboards_list = []

        for i in range(keyboards_number):
            kb_list_at_number_i = []
            variants = self.data[self.data['top_kb_index'] == i+1]
            for j, row in variants.iterrows():
                button_text = get_button_text(row)
                if row['second_kb_index'] < 0:
                    kb_list_at_number_i.append([InlineKeyboardButton(
                        text=button_text, callback_data=AnotherQuestionCallback().pack()
                    )])
                else:
                    kb_list_at_number_i.append([InlineKeyboardButton(
                        text=button_text, 
                        callback_data=SecondLevelCallback(top_kb_index=row['top_kb_index'],
                                                          second_kb_index=row['second_kb_index'],
                                                        next_kb=row['next_kb']
                                                          ).pack())])

            if back_button:
                back_button = add_back_button()
                kb_list_at_number_i.append([back_button])
            self.keyboards_list.append(kb_list_at_number_i)



second_level_kb = SecondLevelKB()



def get_second_level_kb(index: int) -> InlineKeyboardMarkup:
    kb_list = second_level_kb.keyboards_list[index - 1]
    result = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return result
    #return second_level_kb.keyboards[index - 1].as_markup(resize_keyboard=True)




def get_third_level_links(top_kb_index: int, second_kb_index: int) -> str:
    df = second_level_kb.data
    link = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index), 'link'].values[0]
    name = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index), 'name'].values[0]
    if pd.notna(link):
        return TEXT_BEFORE_LINK  + f'<a href="{link}">{name}</a> \n'
    else:
        description = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index), 'description'].values[0]
        return description
    