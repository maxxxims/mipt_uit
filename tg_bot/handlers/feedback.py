from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from keyboards import get_main_kb, reload
from config import MSG_AFTER_FIND_TOPICS, MSG_AFTER_NOT_FOUND
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
import config
import aiohttp
from callbacks import FeedBackCallback, CloseFeedBackCallback
from utils import validate_email
from fsm import FeedBack
from config import  FEEDBACK_MSG_1, FEEDBACK_MSG_2, FEEDBACK_MSG_3, FEEDBACK_MSG_END
from keyboards import get_close_feedback_button
from utils import send_feedback_email
import logging
from aiogram.utils.chat_action import ChatActionSender

router = Router()


@router.callback_query(StateFilter(None), FeedBackCallback.filter())
async def feedback_callback(query: CallbackQuery, state: FSMContext, callback_data: FeedBackCallback):
    kb = get_close_feedback_button()
    await query.message.answer(text=FEEDBACK_MSG_1, reply_markup=kb)
    await query.answer()
    await state.set_state(FeedBack.writing_email)


@router.message(StateFilter(FeedBack.writing_email), F.text)
async def feedback_callback(message: Message, state: FSMContext):
    email = message.text
    if validate_email(email):
        await message.answer(text=FEEDBACK_MSG_2)
        await state.set_state(FeedBack.writing_feedback)
        await state.update_data(email=email)
    else:
        kb = get_close_feedback_button()
        await message.answer(text='Некорректный email, введите ещё раз', reply_markup=kb)


@router.message(StateFilter(FeedBack.writing_feedback), F.text)
async def feedback_callback(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        data = await state.get_data()
        email = data['email']
        result =await send_feedback_email(message.text, email)
        logging.info(f"send msg result = {result}")
    await message.answer(text=FEEDBACK_MSG_3)
    await state.set_state(None)


@router.callback_query(StateFilter('*'), CloseFeedBackCallback.filter()) # FeedBack.writing_email, FeedBack.writing_feedback
async def feedback_callback(query: CallbackQuery, state: FSMContext, callback_data: FeedBackCallback):
    await query.answer()

    current_state = await state.get_state()
    if current_state == FeedBack.writing_email or current_state == FeedBack.writing_feedback:
        await query.message.answer(text=FEEDBACK_MSG_END) 

    await query.message.delete()
    await state.set_state(None)
