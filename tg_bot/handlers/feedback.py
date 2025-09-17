from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from keyboards import get_main_kb, reload
from config import MSG_AFTER_FIND_TOPICS, MSG_AFTER_NOT_FOUND
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
import config
import asyncio
from callbacks import FeedBackCallback, CloseFeedBackCallback, RefreshCallback, FeedBackSendedCallback
from utils import validate_email
from fsm import FeedBack
from config import  FEEDBACK_MSG_1, FEEDBACK_MSG_2, FEEDBACK_MSG_3, FEEDBACK_MSG_END
from keyboards import get_close_feedback_button, get_send_feedback_button
from utils import send_feedback_email, make_attachments, define_file_type
import logging
from aiogram.utils.chat_action import ChatActionSender
from middlewares.feedback_middleware import USERS_TEXTS

MAX_MSG_LIMIT = 10

router = Router()



async def delete_sent_messages(state: FSMContext, message: Message, to_delete: bool = True):
    """Удаляем предыдущие сообщения и оставляем текущее"""
    data = await state.get_data()

    # Формируем корректный текст
    user_attachment_files = data.get('user_attachment_files', [])
    user_attachment_files_clean = [el for el in user_attachment_files if el is not None]
    answer_text = 'Нажмите кнопку "Отправить", чтобы направить обращение в поддержку.'
    n_files = len(user_attachment_files_clean)
    if n_files:
        if n_files == 1:
            answer_text = f'Загружен {len(user_attachment_files_clean)} файл.\n' + answer_text
        elif 1 < n_files < 5:
            answer_text = f'Загружено {len(user_attachment_files_clean)} файла.\n' + answer_text
        else:
            answer_text = f'Загружено {len(user_attachment_files_clean)} файлов.\n' + answer_text

    # отправляем сообщение
    answer_msg = await message.answer(text=answer_text, reply_markup=get_send_feedback_button())
    data = await state.get_data()
    sent_msgs = data.get('sent_msgs', [])
    sent_msgs.append(answer_msg.message_id)
    await state.update_data(sent_msgs=sent_msgs)


    if to_delete:
        # удаляем уже отправленные кроме текущего (актуального)
        data = await state.get_data()
        sent_msgs = data.get('sent_msgs', [])

        for msg_id in sent_msgs:
            if msg_id != answer_msg.message_id:
                try:
                    await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
                except:
                    ...



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
        await message.answer(text=FEEDBACK_MSG_2.split('.')[0] + ':')
        await state.set_state(FeedBack.writing_feedback)
        await state.update_data(email=email)
    else:
        kb = get_close_feedback_button()
        await message.answer(text='Некорректный email, введите ещё раз', reply_markup=kb)


@router.message(StateFilter(FeedBack.writing_feedback))
async def feedback_callback(message: Message, state: FSMContext):
    data = await state.get_data()
    
    user_msg_count = data.get('user_msg_count', 0)
    user_msg_count += 1
    await state.update_data(user_msg_count=user_msg_count)

    # пользователь отправил слишком много сообщений
    if user_msg_count > MAX_MSG_LIMIT:
        await message.answer(text=f'Вы отправили слишком много сообщений, ваш запрос не будет отправлен в поддержку. Попробуйте ещё раз.')
        if message.from_user.id in USERS_TEXTS.keys():
            del USERS_TEXTS[message.from_user.id]   
        # удаляем уже отправленные кроме текущего (актуального)
        data = await state.get_data()
        sent_msgs = data.get('sent_msgs', [])
        for msg_id in sent_msgs:
            try:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
            except:
                ...
        await state.clear()
        return 

    # определяем текст если есть
    user_text = message.text
    if user_text is None:
        user_text = message.caption
    if user_text is None:
        user_text = ''
    
    # пользователь отправил текст
    if user_text != '':
        USERS_TEXTS[message.from_user.id].append(user_text)
    
    # пользователь отправил файл
    attachment_file = define_file_type(message)
    if attachment_file is not None:
        data = await state.get_data()
        user_attachment_files = data.get('user_attachment_files', [])
        user_attachment_files.append(attachment_file)
        await state.update_data(user_attachment_files=user_attachment_files)

    await delete_sent_messages(state=state, message=message, to_delete=False)

    

@router.callback_query(StateFilter('*'), RefreshCallback.filter()) 
async def refresh_feedback_callback(query: CallbackQuery, state: FSMContext, callback_data: FeedBackCallback):
    await query.answer()

    current_state = await state.get_state()
    if current_state != FeedBack.writing_feedback:
        try:
            await query.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        except:
            ...
        return

    await delete_sent_messages(state=state, message=query.message)


@router.callback_query(StateFilter('*'), FeedBackSendedCallback.filter()) 
async def send_feedback_callback(query: CallbackQuery, state: FSMContext, callback_data: FeedBackCallback):
    await query.answer()

    current_state = await state.get_state()
    if not current_state == FeedBack.writing_feedback:
        try:
            await query.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        except:
            ...
        return


    data = await state.get_data()
    await state.set_state(None)

    sent_msgs = data.get('sent_msgs', [])
    for msg_id in sent_msgs:
        try:
            await query.bot.delete_message(chat_id=query.message.chat.id, message_id=msg_id)
        except:
            ...

    await query.message.answer(text=FEEDBACK_MSG_3)
    
    email = data['email']
    user_attachment_files = data.get('user_attachment_files', [])
    user_texts = USERS_TEXTS.get(query.from_user.id, '')

    if len(user_texts) == 0:
        user_text = ''
    else:
        user_text = '\n\n'.join(user_texts)

    attachments = await make_attachments(user_attachment_files, query.bot)
    result = await send_feedback_email(text=user_text, email=email, files=attachments)
    logging.info(f"send msg result = {result}")
    await state.clear()
    if query.from_user.id in USERS_TEXTS.keys():
        del USERS_TEXTS[query.from_user.id]
    

@router.callback_query(StateFilter('*'), CloseFeedBackCallback.filter()) # FeedBack.writing_email, FeedBack.writing_feedback
async def feedback_callback(query: CallbackQuery, state: FSMContext, callback_data: FeedBackCallback):
    await query.answer()

    current_state = await state.get_state()
    if current_state == FeedBack.writing_email or current_state == FeedBack.writing_feedback:
        await query.message.answer(text=FEEDBACK_MSG_END) 

    if query.from_user.id in USERS_TEXTS.keys():
        del USERS_TEXTS[query.from_user.id]
    await query.message.delete()
    await state.set_state(None)
    await state.clear()
