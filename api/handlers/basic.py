import os

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import (
    Message,
    BufferedInputFile
)

from aiogram import (
    Bot,
    types,
    Router,
    F
)
from pydrive.files import FileNotUploadedError
from api.keybords.reply import game_keyboard

from api.handlers.errors_massages import DONT_GET_PHOTO
from api.google_cloud_storage.gcs_service import GoogleCloudStorageService as GCS
from DB.queries import (
    UserActivity,
    PhotoActivity,
)

user_query = UserActivity()
photo_query = PhotoActivity()

user_router = Router()


class ResponsesUser(StatesGroup):
    response_user = State()
    photo = State()


@user_router.message(F.text.casefold() == "start")
async def get_start(message: Message):
    await message.answer(text=f'Hello')

    data = {
        'username': message.from_user.username
    }

    user_query.create_user(data)


@user_router.message(F.photo)
async def upload_photo(message: Message, bot: Bot):
    file_path = str(GCS.get_file_path()) + '/'

    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file_path=file.file_path, destination=f"{file_path}{file.file_id}.png")

    if GCS().create_file(file_name=f"{file.file_id}.png", path=file_path):
        os.remove(file_path + f'{file.file_id}.png')

        data = {'name': f'{file.file_id}.png'}
        photo_query.create_photo(data)

        await message.answer(text='Я успешно сохранил фото')


@user_router.message(StateFilter(ResponsesUser.response_user))
@user_router.message(F.text.casefold() == "start game")
async def get_photo(message: types.Message, state: FSMContext):
    data_state = await state.get_data()

    if message.text.casefold() != "start game":
        photo: list = data_state.get("photo")

        response = ['e34', 'e36', 'e38', 'e49']

        if message.text.casefold() in response:

            if data_state.get('response_user') is None:
                await state.update_data(response_user=[message.text.casefold()])

            else:
                user_responses = data_state.get('response_user')
                user_responses.append(message.text.casefold())

                await state.update_data(response_user=user_responses)

        file_path = os.path.realpath(photo[0].name)
        os.remove(file_path)

        photo.remove(photo[0])

        await state.set_state(ResponsesUser.photo)
        await state.update_data(photo=photo)

        data_state = await state.get_data()

    text1 = 'e34'
    text2 = 'e36'
    text3 = 'e38'
    text4 = 'e49'

    reply = game_keyboard(
        text1,
        text2,
        text3,
        text4
    )

    if len(data_state) == 0:
        data = photo_query.get_photos()

        await state.set_state(ResponsesUser.photo)
        await state.update_data(photo=data)

        data_state = await state.get_data()

    if len(data_state.get('photo')) == 0:
        await message.answer(text='Game over')
        return

    try:
        photo = data_state.get("photo")

        GCS().get_file(file_name=photo[0].name)

        with open(photo[0].name, 'rb') as file:
            data = file.read()
            photo_path = BufferedInputFile(file=data, filename='post')

            await message.answer_photo(photo=photo_path, reply_markup=reply)

            await state.set_state(ResponsesUser.response_user)

    except FileNotUploadedError:
        await message.answer(text='Тех. сбой, я сообщил об этой ошибке разработчикам, скоро это починят')
        return await message.answer(text=DONT_GET_PHOTO)
