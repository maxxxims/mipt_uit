import aiohttp
import config
import jwt

URL = config.load_backend_url()

jwt_token = jwt.encode({'login': 'True'}, config.load_private_key())

async def get_topics_from_keywords(text: str) -> list:
    async with aiohttp.ClientSession() as session:
        json = {'text': text}
        headers = {"Authorization": f"{jwt_token}"}
        print(f'HEADER = {headers}')
        async with session.post(url=f'{URL}/keywords/check', json=json, headers=headers) as response:
            json = await response.json()
            # print(f'json: {json}')
            # print(f'status = {response.status}')

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