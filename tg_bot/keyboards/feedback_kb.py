from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from collections import defaultdict
from callbacks import CloseFeedBackCallback
import emoji
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton


def get_close_feedback_button() -> InlineKeyboardMarkup: 
    return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=emoji.emojize(":cross_mark:")+ "Закрыть",
               callback_data=CloseFeedBackCallback().pack())]]
        )
     