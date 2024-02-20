from db import async_session
from models import Request
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from datetime import datetime


async def add_request(text: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(Request).values(text=text))



async def get_all_requests():
    async with async_session() as session:
        request = (await session.execute(select(Request))).scalars().all()
        return request
    

async def get_requests_in_range(start_date: datetime, end_date: datetime):
    async with async_session() as session:
        request = (await session.execute(select(Request).where(
            Request.date >= start_date, Request.date <= end_date
        ))).scalars().all()
        return request
    