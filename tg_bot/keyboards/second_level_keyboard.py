from .keyboard import KBTemplate, get_button_text, add_back_button, TEXT_BEFORE_LINK, get_formatted_description
import pandas as pd
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from callbacks import *
from collections import defaultdict


class SecondLevelKB(KBTemplate):
    path_to_csv = "data/kb_second_level_oldmipt.csv"
    def make_kb(self, back_button: bool = True) -> None:
        self.data = pd.read_csv(self.path_to_csv, sep=self.sep, na_values=self.na_values)
        self.index_to_keyboard = defaultdict(list)

        for i in self.data['top_kb_index'].unique():
            kb_list_at_number_i = []
            variants = self.data[self.data['top_kb_index'] == i]
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
            self.index_to_keyboard[i] = kb_list_at_number_i
    

    def get_kb(self, index: int) -> list:
        kb_list = self.index_to_keyboard[index]
        result = InlineKeyboardMarkup(
            inline_keyboard=kb_list
        ) 
        return result


second_level_kb = SecondLevelKB()



def get_second_level_kb(index: int) -> InlineKeyboardMarkup:
    # kb_list = second_level_kb.keyboards_list[index - 1]
    # result = InlineKeyboardMarkup(
    #     inline_keyboard=kb_list
    # )
    # return result
    #return second_level_kb.keyboards[index - 1].as_markup(resize_keyboard=True)
    kb = second_level_kb.get_kb(index)
    return kb



def get_third_level_links(top_kb_index: int, second_kb_index: int) -> str:
    df = second_level_kb.data
    selection = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index)]
    return get_formatted_description(selection)
    # link = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index), 'link'].values[0]
    # name = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index), 'name'].values[0]
    # if pd.notna(link):
    #     return TEXT_BEFORE_LINK  + f'<a href="{link}">{name}</a> \n'
    # else:
    #     description = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index), 'description'].values[0]
    #     return description
    