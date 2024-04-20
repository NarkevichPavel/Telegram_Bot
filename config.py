import asyncio
from aiogram import (
    Bot,
    Dispatcher,
)
from api.middlewares.settings import settings

from api.handlers.basic import user_router
from api.handlers.admin import admin_router

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=settings.bots.token)
bot.my_admins_list = []

dp = Dispatcher()

dp.include_router(user_router)
dp.include_router(admin_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())

if __name__ == '__main__':
    asyncio.run(main())
