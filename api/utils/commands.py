from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, Update


async def set_command(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='photo',
            description='Узнай себя поближе'
        )
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
