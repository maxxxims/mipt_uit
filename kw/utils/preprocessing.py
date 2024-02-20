import nltk
nltk.download('stopwords')
import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()



def lemmatize(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            tokens.append(token)
    if len(tokens) > 2:
        return tokens
    return None




def preprocess_request(text: str):
    """
        Preprocess text written by user: \n
        delete special symbols, convert to lower case \n
        CORRECT 1C symbols (language)
    """
    text = text.lower()
    print(f'text = {text}')
    if '1c' in text or '1 c' in text:
        print('here!')
        text += ' 1с'


    SPECIAL_SYMBOLS = ['.',',', ';', '*', ')', '(']
    text = text.replace('-', ' ')
    for symbol in SPECIAL_SYMBOLS:
        text = text.replace(symbol, '')
    text = ' '.join([word for word in text.split() if len(word) > 1 ])

    return text


def add_limmatized_words(text: str):
    lemmatized_words = lemmatize(preprocess_request(text))

    for word in lemmatized_words if lemmatized_words is not None else []:
        text += f' {word}'
    
    return text