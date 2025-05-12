from aiogram.fsm.state import StatesGroup, State


class FeedBack(StatesGroup):
    writing_feedback = State()
    writing_email = State()