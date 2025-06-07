from .keyboard import KBTemplate, get_button_text, add_back_button, TEXT_BEFORE_LINK, get_formatted_description
import pandas as pd
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from callbacks import *



class ThirdLevelKB(KBTemplate):
    path_to_csv = "data/kb_third_level_oldmipt.csv"
    def make_kb(self) -> None:
        self.data = pd.read_csv(self.path_to_csv, sep=self.sep, na_values=self.na_values)
        self.data['description'] = self.data['description'].apply(lambda text: text.replace('**', '\n') if isinstance(text, str) else text)

    def get_kb(self, top_kb_index: int,
                     second_kb_index: int,
                     back_button: bool = True) -> list:
        variants = self.data[(self.data['top_kb_index'] == top_kb_index) & 
                             (self.data['second_kb_index'] == second_kb_index)]
        # kb = InlineKeyboardBuilder()
        kb_list = []
        for j, row in variants.iterrows():
            button_text = get_button_text(row)
            if row['third_kb_index'] < 0:
                pass
                # kb_list.append(
                #     [InlineKeyboardButton(text=button_text, callback_data=AnotherQuestionCallback().pack())]
                # )
                
            elif row['third_kb_index'] == 3 and row['second_kb_index'] == 2 and row['top_kb_index'] == 7:
                kb_list.append(
                    [InlineKeyboardButton(text=button_text, callback_data=TopLevelCallback(top_kb_index=3).pack())]
                )
                
            elif row['third_kb_index'] == 10 and row['second_kb_index'] == 2 and row['top_kb_index'] == 12:
                kb_list.append(
                    [InlineKeyboardButton(text=button_text, callback_data=TopLevelCallback(top_kb_index=11).pack())]
                )

            else:    
                kb_list.append([
                    InlineKeyboardButton(
                        text=button_text,
                        callback_data=ThirdLevelCallback(top_kb_index=row['top_kb_index'],
                                                            second_kb_index=row['second_kb_index'],
                                                            third_kb_index=row['third_kb_index'],
                                                            ).pack())]
                )
        if back_button:
            back_button = add_back_button(top_kb_index=top_kb_index)
            kb_list.append([back_button])
        # add_back_button(kb, top_kb_index=top_kb_index)
        return kb_list
    


third_level_kb = ThirdLevelKB()



def get_third_level_kb(top_kb_index: int, second_kb_index: int) -> InlineKeyboardMarkup:
    kb_list = third_level_kb.get_kb(top_kb_index, second_kb_index)
    return InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )



def get_fourth_level_links(top_kb_index: int, second_kb_index: int, third_kb_index: int) -> str:
    df = third_level_kb.data
    selection = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index) & (df['third_kb_index'] == third_kb_index)]
    return get_formatted_description(selection)
    # link = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index) & (df['third_kb_index'] == third_kb_index), 'link'].values[0]
    # name = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index) & (df['third_kb_index'] == third_kb_index), 'name'].values[0]
    # if pd.notna(link): 
    #     return TEXT_BEFORE_LINK  + f'<a href="{link}">{name}</a> \n'
    # else:
    #     description = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index) & (df['third_kb_index'] == third_kb_index), 'description'].values[0]
    #     return description