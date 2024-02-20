from sanic import Blueprint, Request, json
from sanic_ext import openapi
from openapi import CheckOrphographyRequest
from utils.correct_words import correct_gramma_in_words, CorrectorParams
from utils.preprocessing import add_limmatized_words, preprocess_request
from utils.find_keywords import get_topics
from database import request_table



router = Blueprint("keywords", url_prefix="/keywords")



@router.post("/check")
@openapi.body({"application/json": CheckOrphographyRequest}, required=True)
async def keywords(request: Request):
    print(request.app.ctx.data)
    r = request.json
    params = CorrectorParams(add_first=False, replace_mistakes=True)
    await request_table.add_request(text=r.get('text'))
    prepocessed_text = preprocess_request(r.get('text'))
    corrected_text = await correct_gramma_in_words(request.app, prepocessed_text, params=params)
    lemmatized_text = add_limmatized_words(corrected_text)
    topics = get_topics(lemmatized_text.split())

    return json({
        'prepocessed_text': prepocessed_text,
        'corrected_text': corrected_text,
        'lemmatized_text': lemmatized_text,
        'topics': topics#[{'msg': 'ok'}, {'ale': 'da'}]
    })