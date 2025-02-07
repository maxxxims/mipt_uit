from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import get_main_kb, reload
from config import GREETING_TEXT, GREETING_IMAGE, load_sticker_id, START_GREETING_TEXT
from aiogram.types import FSInputFile

router = Router()

STICKER_ID = load_sticker_id()


@router.message(Command("start"))
async def cmd_start(message: Message):
    kb = get_main_kb()
    await message.answer_sticker(STICKER_ID)
    await message.answer(text=START_GREETING_TEXT, reply_markup=kb)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    kb = get_main_kb()
    await message.answer_sticker(STICKER_ID)
    await message.answer(text=START_GREETING_TEXT, reply_markup=kb)
    #await message.answer(text=GREETING_TEXT, reply_markup=kb)


@router.message(Command("reload"))
async def cmd_reload(message: Message):
    if message.from_user.id == 6161416635:
        reload()
    else:
        print(message.from_user.id)
    