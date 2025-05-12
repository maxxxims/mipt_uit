from aiogram.filters.callback_data import CallbackData

class FeedBackCallback(CallbackData, prefix="feedback"):
    ...

class CloseFeedBackCallback(CallbackData, prefix="close_feedback"):
    ...