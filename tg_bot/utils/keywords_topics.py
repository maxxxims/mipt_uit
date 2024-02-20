import aiohttp
import config

URL = config.load_backend_url()


async def get_topics_from_keywords(text: str) -> list:
    async with aiohttp.ClientSession() as session:
        json = {
            'token': 'kakou-to token',
            'text': text,
        }
        async with session.post(url=f'{URL}/keywords/check', json=json) as response:
            json = await response.json()
            print(f'json: {json}')
            print(f'status = {response.status}')

    if len(json.get('topics', [])) > 0:
        return json.get('topics')
    
    else:
        return None
    

    # string = ''
    # topics = json.get('topics', [])
    # for el in topics:
    #     string += f"{el['name'], el['third_kb_index']}"
    # await message.answer(text=f'Найденные темы: \n{string}'
    # )   