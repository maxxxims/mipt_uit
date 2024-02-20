import aiohttp
from sanic import Sanic

class CorrectorParams:
    def __init__(self, add_first: bool = False,
                  replace_mistakes: bool = True):
        self.add_first = add_first
        self.replace_mistakes = replace_mistakes


async def request_to_corrector(app: Sanic, words: str) -> dict:
    MAX_TEXT_LEN = 10000
    if len(words) > MAX_TEXT_LEN:
        words = words[:MAX_TEXT_LEN - 1]

    async with aiohttp.ClientSession() as session:
        data = {
            'lang': 'ru, en',
            'format': 'plain',
            'text': words,
        }
        async with session.post(app.ctx.YANDEX_URL, data=data) as response:
            json = await response.json()
            print(json)
            if response.status != 200:
                return None
            if json is not None:
                if len(json) != 0:
                    return json
            return None
        


async def correct_gramma_in_words(app: Sanic, words: str, params: CorrectorParams) -> str:
    """
        corrects grammatical errors in words entered by the user using the Yandex service \n
        return: str, single space
    """
    response = await request_to_corrector(app, words)
    if response is None:
        return words
    for word_list in response:
        if len(word_list.get('s', [])) == 0:
            continue

        if params.add_first:
            words += f" {word_list.get('s')[0]}"

        else:
            print('HERE!')
            for word in word_list.get('s'):
                #print(f'{word}')
                words += f' {word}'

        if params.replace_mistakes :  #and len(word_list.get('word', '')) > 0
            print(f'replaced word = {word_list.get("word")}')
            words = words.replace(word_list.get('word'), "")
    return ' '.join(words.split())