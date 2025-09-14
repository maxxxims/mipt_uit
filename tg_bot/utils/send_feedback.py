import aiohttp
import config
import jwt
from aiogram.types import Message
from aiogram import Bot


URL = config.load_backend_url()

jwt_token = jwt.encode({'login': 'True'}, config.load_private_key())


async def add_file(attachments: list, file: dict, bot: Bot):
    file_info = await bot.get_file(file['file_id'])
    file_data = await bot.download_file(file_info.file_path)
    file_data = file_data.read().hex()
    attachments.append(('photo', file['file_name'], file_data))


async def make_attachments(files: list, bot: Bot) -> list:
    attachments = []
    for file in files:
        if file is not None:
            await add_file(attachments, file, bot)
    return attachments


def define_file_type(message: Message) -> dict:
    if message.photo is not None:
        dtype = 'photo'
        file_id = message.photo[-1].file_id
        file_name = f"photo_{file_id}.jpg"
    elif message.document is not None:
        dtype = 'document'
        file_id = message.document.file_id
        file_name = message.document.file_name
    elif message.video is not None:
        dtype = 'video'
        file_id = message.video.file_id
        file_name = message.video.file_name
    else:
        return None
    return {'dtype': dtype, 'file_id': file_id, 'file_name': file_name}


async def send_feedback_email(text: str, email: str, files: list = None) -> bool:
    async with aiohttp.ClientSession() as session:
        if files is None:
            files = []
            
        json = {'text': text,
                'user_email': email,
                'files': files
                }
        headers = {"Authorization": f"Bearer {jwt_token}"}
        # print(f'HEADER = {headers}')
        async with session.post(url=f'{URL}/email/send', json=json, headers=headers) as response:
            json = await response.json()
    return json.get('status', None)