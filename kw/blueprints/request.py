from sanic import Blueprint, Request, json
from sanic_ext import openapi, render
from openapi import CheckOrphographyRequest
from utils.correct_words import correct_gramma_in_words, CorrectorParams
from utils.preprocessing import add_limmatized_words, preprocess_request
from utils.find_keywords import get_topics
from database import request_table
import pandas as pd
from datetime import datetime

router = Blueprint("request", url_prefix="/request")


@router.get("/")
async def show_request_table(request: Request):
    users_requests = await request_table.get_all_requests()
    requests_list = []
    for r in users_requests:
        temp = {}
        temp['id'] = r.__dict__['id']
        temp['text'] = r.__dict__['text']
        temp['date'] = r.__dict__['date'].replace(microsecond=0)
        requests_list.append(temp)
    # print(requests_list)
    return await render("requests_table.html",
                        context={'requests_list': requests_list})


@router.post("/make_file")
async def make_request_table(request: Request):
    users_requests = await request_table.get_all_requests()
    requests_list = []
    for r in users_requests:
        requests_list.append(r.__dict__)
    df = pd.DataFrame(requests_list, columns=['text', 'date'])

    with pd.ExcelWriter("data/requests.xlsx") as writer:
        df.to_excel(writer, sheet_name="Запросы пользователей", index=False)
    return json({"status": 200})