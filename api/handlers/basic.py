from aiogram.types import Message


async def get_start(message: Message):
    await message.answer(text=f'Hello {message.from_user.full_name}')
