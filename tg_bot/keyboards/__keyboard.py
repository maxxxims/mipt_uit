from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from collections import defaultdict
from callbacks import TopLevelCallback, SecondLevelCallback, BackButtonCallback, AnotherQuestionCallback, \
                      ThirdLevelCallback
import pandas as pd
import emoji


TEXT_BEFORE_LINK = 'Ссылка по вашему запросу:\n'

def add_back_button(kb: InlineKeyboardBuilder, top_kb_index: int = -1):
    if top_kb_index < 0:
        level = 'top'
    else:
        level = 'second'
    kb.button(text=emoji.emojize(":BACK_arrow:")+"Назад",
               callback_data=BackButtonCallback(top_kb_index=top_kb_index, level=level).pack())


def get_button_text(row: pd.Series):
    text_emoji = ''
    if pd.notna(row['emoji']):
        text_emoji = emoji.emojize(row['emoji']) + ' '
    return text_emoji + row['name']


class KBTemplate():
    adjust = 1
    sep = ';'
    na_values='None'
    def __init__(self) -> None:
        self.make_kb()

    def reload(self):
        self.make_kb()


class MainKB(KBTemplate):
    path_to_csv = "data/kb_top_level.csv"
    def make_kb(self):
        data = pd.read_csv(self.path_to_csv, sep=self.sep, na_values=self.na_values)
        self.kb = InlineKeyboardBuilder()
        for i, row in data.iterrows():
            button_text = get_button_text(row)
            if row['top_kb_index'] < 0:
                self.kb.button(text=button_text, 
                               callback_data=AnotherQuestionCallback().pack())
            else:
                self.kb.button(text=button_text, 
                            callback_data=TopLevelCallback(top_kb_index=row['top_kb_index']).pack())
        self.kb.adjust(self.adjust)


class SecondLevelKB(KBTemplate):
    path_to_csv = "data/kb_second_level_oldmipt.csv"
    def make_kb(self) -> None:
        self.data = pd.read_csv(self.path_to_csv, sep=self.sep, na_values=self.na_values)
        keyboards_number = len(self.data['top_kb_index'].unique())
        self.keyboards = [InlineKeyboardBuilder() for _ in range(keyboards_number)] 
        for i, kb in enumerate(self.keyboards):
            variants = self.data[self.data['top_kb_index'] == i+1]
            for j, row in variants.iterrows():
                button_text = get_button_text(row)
                if row['second_kb_index'] < 0:
                    kb.button(text=button_text, 
                                callback_data=AnotherQuestionCallback().pack())
                else:    
                    kb.button(text=button_text, 
                                callback_data=SecondLevelCallback(top_kb_index=row['top_kb_index'],
                                                                second_kb_index=row['second_kb_index'],
                                                                next_kb=row['next_kb']
                                                                ).pack())
            add_back_button(kb)
            kb.adjust(self.adjust)



class ThirdLevelKB(KBTemplate):
    path_to_csv = "data/kb_third_level_oldmipt.csv"
    def make_kb(self) -> None:
        self.data = pd.read_csv(self.path_to_csv, sep=self.sep, na_values=self.na_values)
    
    def get_kb(self, top_kb_index: int, second_kb_index: int) -> InlineKeyboardMarkup:
        variants = self.data[(self.data['top_kb_index'] == top_kb_index) & 
                             (self.data['second_kb_index'] == second_kb_index)]
        kb = InlineKeyboardBuilder()
        for j, row in variants.iterrows():
            button_text = get_button_text(row)
            if row['third_kb_index'] < 0:
                kb.button(text=button_text, 
                            callback_data=AnotherQuestionCallback().pack())
                
            elif row['third_kb_index'] == 3 and row['second_kb_index'] == 2 and row['top_kb_index'] == 6:
                kb.button(text=button_text, 
                            callback_data=TopLevelCallback(top_kb_index=2,
                                                            ).pack())
            else:    
                kb.button(text=button_text, 
                            callback_data=ThirdLevelCallback(top_kb_index=row['top_kb_index'],
                                                            second_kb_index=row['second_kb_index'],
                                                            third_kb_index=row['third_kb_index'],
                                                            ).pack())
        add_back_button(kb, top_kb_index=top_kb_index)
        kb.adjust(self.adjust)
        return kb.as_markup(resize_keyboard=True)
        

# MAKE KB
main_kb = MainKB()
second_level_kb = SecondLevelKB()
third_level_kb = ThirdLevelKB()


def reload():
    main_kb.reload()
    second_level_kb.reload()
    third_level_kb.reload()


def get_main_kb() -> ReplyKeyboardMarkup:
    return main_kb.kb.as_markup(resize_keyboard=True)


def get_second_level_kb(index: int) -> ReplyKeyboardMarkup:
    return second_level_kb.keyboards[index - 1].as_markup(resize_keyboard=True)


def get_third_level_kb(top_kb_index: int, second_kb_index: int) -> InlineKeyboardMarkup:
    return third_level_kb.get_kb(top_kb_index, second_kb_index)


def get_third_level_links(top_kb_index: int, second_kb_index: int) -> str:
    df = SecondLevelKB().data
    link = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index), 'link'].values[0]
    name = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index), 'name'].values[0]
    if pd.notna(link):
        return TEXT_BEFORE_LINK  + f'<a href="{link}">{name}</a> \n'
    else:
        description = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index), 'description'].values[0]
        return description
    


def get_fourth_level_links(top_kb_index: int, second_kb_index: int, third_kb_index: int) -> str:
    df = ThirdLevelKB().data
    link = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index) & (df['third_kb_index'] == third_kb_index), 'link'].values[0]
    name = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index) & (df['third_kb_index'] == third_kb_index), 'name'].values[0]
    if pd.notna(link): 
        return TEXT_BEFORE_LINK  + f'<a href="{link}">{name}</a> \n'
    else:
        description = df.loc[(df['top_kb_index'] == top_kb_index) & (df['second_kb_index'] == second_kb_index) & (df['third_kb_index'] == third_kb_index), 'description'].values[0]
        return description