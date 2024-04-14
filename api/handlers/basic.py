from aiogram.types import Message, BufferedInputFile
from aiogram import Bot, types
from api.middlewares.settings import settings
from api.google_cloud_storage.gcs_service import GoogleCloudStorageService as GCS
import os


async def get_start(message: Message):
    await message.answer(text=f'Hello {message.from_user.id}')


async def get_message(message: Message):
    if message.from_user.id == settings.bots.admin_id:
        return await message.answer(text='Good')


async def upload_photo(message: Message, bot: Bot):
    file_path = 'C:/Users/USER/Telegram_Bot/api/google_cloud_storage/'

    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file_path=file.file_path, destination=f"{file_path}{file.file_id}.png")

    GCS().create_file(file_name=f"{file.file_id}.png", path=file_path)

    os.remove(file_path + f'{file.file_id}.png')

    await message.answer(text='Я успешно сохранил фото')


async def get_photo(message: types.Message):


    with open('AgACAgIAAxkBAAICAAFl_Iq7gcGLLzDIjv2c-sf64MGfywACqNoxG-RR4UuMpoyVTCgrdAEAAwIAA3kAAzQE.png', 'rb') as file:
        data = file.read()
        photo_path = BufferedInputFile(file=data, filename='post')

        await message.answer_photo(photo=photo_path)

    file_path = os.path.realpath('AgACAgIAAxkBAAICAAFl_Iq7gcGLLzDIjv2c-sf64MGfywACqNoxG-RR4UuMpoyVTCgrdAEAAwIAA3kAAzQE.png')
    os.remove(file_path)
