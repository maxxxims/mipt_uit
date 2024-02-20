from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile
from keyboards import get_main_kb, get_second_level_kb, get_third_level_links, get_third_level_kb, \
                      get_fourth_level_links
from callbacks import TopLevelCallback, BackButtonCallback, SecondLevelCallback, AnotherQuestionCallback, \
                      ThirdLevelCallback
from utils import another_question, ANOTHER_QUESTION_INDEX
from config import GREETING_TEXT, DEFAULT_TEXT, GREETING_IMAGE
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext



router = Router()
#GREETING_TEXT = """Здравствуйте! \nЭтот чат-бот поможет в поиске нужного IT-сервиса МФТИ. Пожалуйста выберите тему из списка."""



@router.callback_query(StateFilter('*'), TopLevelCallback.filter())
async def top_level_callback(query: CallbackQuery,  state: FSMContext, callback_data: TopLevelCallback):
    kb = get_second_level_kb(callback_data.top_kb_index)
    try:    await query.message.delete()
    except: await query.answer()
    await query.message.answer(text=DEFAULT_TEXT, 
                                reply_markup=kb)
    

@router.callback_query(StateFilter('*'), SecondLevelCallback.filter(F.next_kb == True))
async def second_level_callback_kb(query: CallbackQuery, state: FSMContext, callback_data: SecondLevelCallback):
    kb = get_third_level_kb(callback_data.top_kb_index, callback_data.second_kb_index)
    try:    await query.message.delete()
    except: await query.answer()
    await query.message.answer(text=DEFAULT_TEXT, 
                               reply_markup=kb)
    

@router.callback_query(StateFilter('*'), SecondLevelCallback.filter(F.next_kb == False))
async def second_level_callback_links(query: CallbackQuery, state: FSMContext, callback_data: SecondLevelCallback):
    msg = get_third_level_links(callback_data.top_kb_index, callback_data.second_kb_index)
    await query.message.answer(text=msg)
    await query.answer()


@router.callback_query(StateFilter('*'), ThirdLevelCallback.filter())
async def second_level_callback(query: CallbackQuery, state: FSMContext, callback_data: ThirdLevelCallback):
    msg = get_fourth_level_links(top_kb_index=int(callback_data.top_kb_index),
                                                                    second_kb_index=callback_data.second_kb_index,
                                                                    third_kb_index=callback_data.third_kb_index)
    await query.message.answer(text=msg)
    await query.answer()


@router.callback_query(StateFilter('*'), BackButtonCallback.filter(F.level == 'top'))
async def back_callback_top_level(query: CallbackQuery, state: FSMContext, callback_data: BackButtonCallback):
    kb = get_main_kb()
    try:    await query.message.delete()
    except: await query.answer()
    await query.message.answer(text=GREETING_TEXT, 
                               reply_markup=kb)###############
    #photo = FSInputFile("data/greeting_image.jpg")
    #await query.message.answer_photo(photo=GREETING_IMAGE, caption=GREETING_TEXT, reply_markup=kb)
    

@router.callback_query(StateFilter('*'), BackButtonCallback.filter(F.level == 'second'))
async def back_callback_second_level(query: CallbackQuery, state: FSMContext, callback_data: BackButtonCallback):
    kb = get_second_level_kb(callback_data.top_kb_index)
    try:    await query.message.delete()
    except: await query.answer()
    await query.message.answer(text=DEFAULT_TEXT, 
                                   reply_markup=kb)