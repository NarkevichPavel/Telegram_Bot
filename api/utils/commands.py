from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, Update


async def set_command(bot: Bot):
    commands = [
        BotCommand(
            command='menu',
            description='Меню.'
        )
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
