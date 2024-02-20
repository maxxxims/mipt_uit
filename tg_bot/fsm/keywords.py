from aiogram.fsm.state import StatesGroup, State


class Keywords(StatesGroup):
    writing_request = State()