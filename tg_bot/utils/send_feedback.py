import aiohttp
import config
import jwt

URL = config.load_backend_url()

jwt_token = jwt.encode({'login': 'True'}, config.load_private_key())


async def send_feedback_email(text: str, email: str) -> bool:
    async with aiohttp.ClientSession() as session:
        json = {'text': text,
                'user_email': email
                }
        headers = {"Authorization": f"Bearer {jwt_token}"}
        # print(f'HEADER = {headers}')
        async with session.post(url=f'{URL}/email/send', json=json, headers=headers) as response:
            json = await response.json()
    return json.get('status', None)