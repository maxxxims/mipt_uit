from db import async_session
from models import Request
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload



async def add_request(text: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(Request).values(text=text))



async def get_all_requests():
    async with async_session() as session:
        request = (await session.execute(select(Request))).scalars().all()
        return request