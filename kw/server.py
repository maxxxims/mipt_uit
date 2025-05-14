import pandas as pd
from sanic import Sanic
from blueprints import keywords, request, send_email
import config
from db import init_db
import os
from utils.find_keywords import load_keywords_df, get_kw2idx
from aiosmtplib import SMTP 
from sanic_ext import Extend
from orjson import loads
import orjson


def best_dumps(obj):
    if isinstance(obj, list):
        return orjson.dumps(list(map(dict, obj)))
    return orjson.dumps(obj)


app = Sanic("TG_BOT_API", ) # dumps=best_dumps, loads=loads

app.ext.openapi.add_security_scheme(
        "token",
        "http",
        scheme="bearer",
        bearer_format="JWT",
    )


app.config.SECRET = config.load_private_key()
app.blueprint(keywords.router)
app.blueprint(request.router)
app.blueprint(send_email.router)

dir_path = os.path.dirname(os.path.realpath(__file__))
app.static('/static', dir_path + r'/static')

@app.before_server_start
async def init(app1: Sanic):
    await init_db()

    app1.ctx.__setattr__('data', "some information")
    app1.ctx.__setattr__('YANDEX_URL', config.LINK_TO_YANDEX_SPELLER)
    app1.ctx.__setattr__('request_xlsx_path', "kw/data/requests.xlsx")
    app1.ctx.__setattr__('keywords_xlsx_path', "kw/data/keywords.xlsx")
    df = load_keywords_df(app1.ctx.keywords_xlsx_path)
    kw2idx = get_kw2idx(df)
    app1.ctx.__setattr__('df', df)
    app1.ctx.__setattr__('kw2idx', kw2idx)

    # print(config.load_email_login(), config.load_email_password())
    # print(config.load_private_key())
    smtp = SMTP(hostname=config.load_smtp_server(), port=config.load_smtp_port(),
                username=config.load_email_login(), password=config.load_email_password(), use_tls=True, validate_certs=False)
    app1.ctx.__setattr__('SMTP', smtp)
    app1.ctx.__setattr__('email_login', config.load_email_login())
    app1.ctx.__setattr__('email_support', config.load_email_support_login())





if __name__ == "__main__":
    HOST = config.load_backend_host()
    PORT = config.load_backend_port()
    # logging.info(f'SWAGGER AVAILABLE AT: http://{HOST}:{PORT}/docs/swagger')
    # logging.info(f"PAGE WITH USERS' REQUESTS: http://{HOST}:{PORT}/request")
    app.run(host=HOST, port=PORT)  # fast=True)