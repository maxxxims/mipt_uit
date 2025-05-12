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

router = Router()


@router.callback_query(StateFilter(None), FeedBackCallback.filter())
async def feedback_callback(query: CallbackQuery, state: FSMContext, callback_data: FeedBackCallback):
    kb = get_close_feedback_button()
    await query.message.answer(text=FEEDBACK_MSG_1, reply_markup=kb)
    await query.answer()
    await state.set_state(FeedBack.writing_feedback)



@router.message(StateFilter(FeedBack.writing_feedback), F.text)
async def feedback_callback(message: Message, state: FSMContext):
    kb = get_close_feedback_button()
    await message.answer(text=FEEDBACK_MSG_2, reply_markup=kb)
    await state.set_state(FeedBack.writing_email)


@router.message(StateFilter(FeedBack.writing_email), F.text)
async def feedback_callback(message: Message, state: FSMContext):
    if validate_email(message.text):
        await message.answer(text=FEEDBACK_MSG_3)
        await state.set_state(None)
    else:
        await message.answer(text='Некорректный email, введите ещё раз')



@router.callback_query(StateFilter('*'), CloseFeedBackCallback.filter()) # FeedBack.writing_email, FeedBack.writing_feedback
async def feedback_callback(query: CallbackQuery, state: FSMContext, callback_data: FeedBackCallback):
    await query.answer()

    current_state = await state.get_state()
    if current_state == FeedBack.writing_email or current_state == FeedBack.writing_feedback:
        await query.message.answer(text=FEEDBACK_MSG_END) 

    await query.message.delete()
    await state.set_state(None)
