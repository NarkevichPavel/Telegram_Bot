import asyncio
from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram import F

from api.handlers.basic import get_start, get_message, get_photo, upload_photo
from api.middlewares.settings import settings

from aiogram.filters import Command
from api.utils.commands import set_command


async def start_bot(bot: Bot):
    await set_command(bot)
    await bot.send_message(chat_id=settings.bots.admin_id, text='Бот успешно запущен')


async def close_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bots.admin_id, text='Бот успешно выключен')


async def start():
    bot = Bot(token=settings.bots.token)

    dp = Dispatcher()

    dp.startup.register(callback=start_bot)
    dp.shutdown.register(callback=close_bot)

    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(get_message, Command(commands='admin'))
    dp.message.register(upload_photo, F.photo)
    dp.message.register(get_photo, Command(commands='photo'))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
