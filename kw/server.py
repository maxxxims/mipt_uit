from sanic import Sanic
from sanic_ext import Extend
from blueprints import keywords, request
import config
from db import init_db
import os
from utils.find_keywords import load_keywords_df, get_kw2idx


app = Sanic("TG_BOT_API")
app.blueprint(keywords.router)
app.blueprint(request.router)


dir_path = os.path.dirname(os.path.realpath(__file__))
app.static('/static', dir_path + r'/static')

print(dir_path)

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
    
    
if __name__ == "__main__":
    app.run(host=config.load_backend_host(),
            port=config.load_backend_port(), dev=True)  # fast=True)