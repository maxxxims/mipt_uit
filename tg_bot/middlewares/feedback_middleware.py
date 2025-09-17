from functools import wraps
from aiogram import Router
from aiogram.fsm.context import FSMContext
from fsm import FeedBack
from aiogram import Bot
from config import FEEDBACK_MSG_END
from collections import defaultdict

USERS_TEXTS  = defaultdict(list)



from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

class CloseFeedbackMiddleware(BaseMiddleware):
    def __init__(self, feedback_states: list = None):
        self.feedback_states = feedback_states or [FeedBack.writing_email, FeedBack.writing_feedback]
        super().__init__()

    async def __call__(
        self,
        handler: Callable,
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        state: FSMContext = data.get('state')
        current_state = await state.get_state()
        bot: Bot = data.get('bot')  # Получаем бота из данных

        is_feedback = False
        for el in self.feedback_states:
            if current_state == el:
                is_feedback = True
                break
        
        if is_feedback:
            if bot:
                await bot.send_message(
                    chat_id=event.from_user.id,
                    text=FEEDBACK_MSG_END
                )
            res = await handler(event, data)
            await state.set_state(None)
            await state.clear()
            if event.from_user.id in USERS_TEXTS.keys():
                del USERS_TEXTS[event.from_user.id] 
            # Используем бота для отправки сообщения
        else:
            res = await handler(event, data)
        return res