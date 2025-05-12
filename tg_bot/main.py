from config import load_token
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from handlers import navigations, commands, keywords, feedback
import logging
logging.basicConfig(level=logging.INFO)


def get_bot_commands():
    bot_commands = [
        types.BotCommand(command="/menu", description="В главное меню"),
    ]
    return bot_commands

async def main():
    token = load_token()
    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_routers(navigations.router, commands.router, keywords.router, feedback.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=get_bot_commands())
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())