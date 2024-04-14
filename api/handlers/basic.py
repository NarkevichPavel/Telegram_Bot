from aiogram.types import Message, BufferedInputFile
from aiogram import Bot, types
from pydrive.files import FileNotUploadedError

from api.handlers.errors_massages import DONT_GET_PHOTO
from api.middlewares.settings import settings
from api.google_cloud_storage.gcs_service import GoogleCloudStorageService as GCS
import os
from DB.queries import UserActivity, PhotoActivity

user_query = UserActivity()
photo_query = PhotoActivity()

bot = Bot(token=settings.bots.token)


async def get_start(message: Message):
    await message.answer(text=f'Hello {message.from_user.id}')

    data = {
        'username': message.from_user.username
    }

    user_query.create_user(data)


async def get_message(message: Message):
    if message.from_user.id == settings.bots.admin_id:
        return await message.answer(text='Good')


async def upload_photo(message: Message, bot: Bot):
    file_path = str(GCS.get_file_path()) + '/'

    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file_path=file.file_path, destination=f"{file_path}{file.file_id}.png")

    if GCS().create_file(file_name=f"{file.file_id}.png", path=file_path):
        os.remove(file_path + f'{file.file_id}.png')

        data = {'name': f'{file.file_id}.png'}
        photo_query.create_photo(data)

        await message.answer(text='Я успешно сохранил фото')


async def get_photo(message: types.Message):
    data = photo_query.get_photos()

    for photo in data:
        try:
            GCS().get_file(file_name=photo.name)
            with open(photo.name, 'rb') as file:
                data = file.read()
                photo_path = BufferedInputFile(file=data, filename='post')

                await message.answer_photo(photo=photo_path)

            file_path = os.path.realpath(photo.name)
            os.remove(file_path)
        except FileNotUploadedError:
            await message.answer(text='Тех. сбой, я сообщил об этой ошибке разработчикам, скоро это починят')
            return await get_error_message(error=DONT_GET_PHOTO, bot=bot)


async def get_error_message(bot: Bot, error: str):
    await bot.send_message(chat_id=settings.bots.admin_id, text=error)
