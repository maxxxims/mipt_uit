from sanic import Blueprint, Request, json, response
from sanic_ext import openapi, render
from openapi import SendEmail
from utils.send_email import send_email
from utils import protected
from sanic_ext.extensions.openapi.definitions import RequestBody

router = Blueprint("email", url_prefix="/email")


@router.post("/send")
@openapi.secured("token")
@openapi.body(RequestBody({"application/json": SendEmail}, required=True))
async def keywords(request: Request):
    r = request.json
    is_sent = await send_email(request.app, text=r.get('text'), user_email=r.get('user_email'))
    return json({
        'status': is_sent,
    })