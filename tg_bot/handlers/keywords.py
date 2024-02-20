from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from keyboards import get_main_kb, reload
from config import MSG_AFTER_FIND_TOPICS, MSG_AFTER_NOT_FOUND
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
import config
import aiohttp
from callbacks import AnotherQuestionCallback, CloseRecommendationKBCallback, NothingFindingCallback
from utils import get_topics_from_keywords, get_kb_from_topics, another_question
from fsm import Keywords
from config import  MSG_ANOTHER_QUESTION

router = Router()


@router.callback_query(StateFilter('*'), AnotherQuestionCallback.filter())
async def another_question_callback(query: CallbackQuery, state: FSMContext, callback_data: AnotherQuestionCallback):
    await query.message.answer(text=MSG_ANOTHER_QUESTION)
    await query.answer()
    await state.set_state(Keywords.writing_request)


@router.callback_query(StateFilter('*'), NothingFindingCallback.filter())
async def close_topics(query: CallbackQuery, state: FSMContext, callback_data: NothingFindingCallback):
    await query.answer()
    await query.message.answer(
        text=MSG_AFTER_NOT_FOUND,
    )
    try:    await query.message.delete()
    except: ...
    await state.set_state(None)


@router.callback_query(StateFilter('*'), CloseRecommendationKBCallback.filter())
async def close_topics(query: CallbackQuery, state: FSMContext, callback_data: CloseRecommendationKBCallback):
    await query.answer()
    try:    await query.message.delete()
    except: ...
    await state.set_state(None)




@router.message(Keywords.writing_request, F.text)
async def find_topics_by_kw(message: Message, state: FSMContext):
    if message.text is None:
        return
    if message.text.startswith('/'):
        return 
    
    sent_msg = await message.answer('Начинаем подбор тем...')
    
    topics = await get_topics_from_keywords(text=message.text)
    if topics is None:
        await sent_msg.delete()
        await message.answer(text=MSG_AFTER_NOT_FOUND)
        await state.set_state(None)
        return
    
    kb = get_kb_from_topics(topics=topics)
    await sent_msg.delete()

    await message.answer(
        text=MSG_AFTER_FIND_TOPICS,
        reply_markup=kb
    )
    await state.set_state(None)