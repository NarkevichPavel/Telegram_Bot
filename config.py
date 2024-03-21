import asyncio
from aiogram import (
    Bot,
    Dispatcher,

)

from api.handlers.basic import get_start
from api.middlewares.settings import settings


async def start():
    bot = Bot(token=settings.bots.token)

    dp = Dispatcher()
    dp.message.register(get_start)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
