from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_command(bot: Bot):
    commands = [
        BotCommand(
            command='/start_game',
            description='Начать игру.'
        )
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
