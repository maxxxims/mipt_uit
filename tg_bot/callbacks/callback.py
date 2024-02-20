from aiogram.filters.callback_data import CallbackData
from typing import Union

class TopLevelCallback(CallbackData, prefix="top_level"):
    top_kb_index: int


class SecondLevelCallback(CallbackData, prefix="second_level"):
    top_kb_index: int
    second_kb_index: int
    next_kb: bool


class ThirdLevelCallback(CallbackData, prefix="third_level"):
    top_kb_index: int
    second_kb_index: int
    third_kb_index: int


class AnotherQuestionCallback(CallbackData, prefix="another"):
    ...


class BackButtonCallback(CallbackData, prefix="back"):
    top_kb_index: int
    level: str