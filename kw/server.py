import pandas as pd
from sanic import Sanic
from blueprints import keywords, request
import config
from db import init_db
import os
import jwt
from pathlib import Path
from utils import get_kw2idx, proccess_kw
import logging
logging.basicConfig(level=logging.INFO)


app = Sanic("TG_BOT_API")
app.config.SECRET = config.load_private_key()
app.blueprint(keywords.router)
app.blueprint(request.router)


dir_path = os.path.dirname(os.path.realpath(__file__))
app.static('/static', dir_path + r'/static')


@app.before_server_start
async def init(_app: Sanic):
    await init_db()

    _app.ctx.__setattr__('YANDEX_URL', config.LINK_TO_YANDEX_SPELLER)
    _app.ctx.__setattr__('request_xlsx_path', Path("kw/data/requests.xlsx"))

    # KEYWORDS INFORMATION
    df = pd.read_excel('kw/data/keywords.xlsx')
    df['keywords'] = df['keywords'].apply(proccess_kw)
    kw2idx = get_kw2idx(df)
    _app.ctx.__setattr__('kw2idx', kw2idx)
    _app.ctx.__setattr__('df', df)

    # JWT TOKEN
    path_to_token = Path('token.txt')
    if not path_to_token.exists():
        jwt_token = jwt.encode({'login': 'True'}, _app.config.SECRET)
        with open(path_to_token, 'w') as f:
            f.write(jwt_token)  
        

if __name__ == "__main__":
    HOST = config.load_backend_host()
    PORT = config.load_backend_port()
    # logging.info(f'SWAGGER AVAILABLE AT: http://{HOST}:{PORT}/docs/swagger')
    # logging.info(f"PAGE WITH USERS' REQUESTS: http://{HOST}:{PORT}/request")
    app.run(host=HOST, port=PORT, dev=True)  # fast=True)