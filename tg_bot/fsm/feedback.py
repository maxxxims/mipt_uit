from aiogram.fsm.state import StatesGroup, State


class FeedBack(StatesGroup):
    writing_email = State()
    writing_feedback = State()
    