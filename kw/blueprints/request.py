from sanic import Blueprint, Request, json, response
from sanic_ext import openapi, render
from openapi import MakeFile
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
    return await render("requests_table.html",
                        context={'requests_list': requests_list})


@router.post("/make_file_in_range")
@openapi.body({"application/form": MakeFile}, required=True)
async def make_request_table_in_range(request: Request):
    form = request.form
    print(f'dates: = {form.get("start_date")}, {form.get("end_date")}; download_all = ')

    if form.get("start_date") is None or form.get("end_date") is None:
        users_requests = await request_table.get_all_requests()
    else:
        users_requests = await request_table.get_requests_in_range(form.get("start_date"),
                                                                    form.get("end_date")
                                                                    )
    requests_list = []
    for r in users_requests:
        print(f'REQUEST = {r.__dict__}')
        requests_list.append(r.__dict__)
    df = pd.DataFrame(requests_list, columns=['text', 'date'])
    path_to_file = request.app.ctx.request_xlsx_path
    with pd.ExcelWriter(path_to_file) as writer:
        df.to_excel(writer, sheet_name="Запросы пользователей", index=False)
    return await response.file_stream(
        location=path_to_file, filename='Таблица с запросами.xlsx'
    )



@router.post("/make_file")
async def make_request_table(request: Request):
    users_requests = await request_table.get_all_requests()
    requests_list = []
    for r in users_requests:
        requests_list.append(r.__dict__)
    df = pd.DataFrame(requests_list, columns=['text', 'date'])
    path_to_file = request.app.ctx.request_xlsx_path
    with pd.ExcelWriter(path_to_file) as writer:
        df.to_excel(writer, sheet_name="Запросы пользователей", index=False)
    return await response.file_stream(
        location=path_to_file, filename='Таблица с запросами.xlsx'
    )