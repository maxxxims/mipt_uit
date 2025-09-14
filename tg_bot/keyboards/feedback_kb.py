from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup
from collections import defaultdict
from callbacks import CloseFeedBackCallback, RefreshCallback, FeedBackSendedCallback
import emoji
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton


def get_close_feedback_button() -> InlineKeyboardMarkup: 
    return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=emoji.emojize(":cross_mark:")+ "Закрыть",
               callback_data=CloseFeedBackCallback().pack())]]
        )
     

def get_send_feedback_button() -> InlineKeyboardMarkup: 
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=emoji.emojize(":counterclockwise_arrows_button:")+ "Обновить файлы",
                        callback_data=RefreshCallback().pack()
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=emoji.emojize(":check_mark_button:")+ "Отправить",
                        callback_data=FeedBackSendedCallback().pack() #white_check_mark
                    )
                ]
            ]
        )