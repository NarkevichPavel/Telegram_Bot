import os

from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message,
    BufferedInputFile
)

from aiogram import (
    types,
    Router,
    F
)
from pydrive.files import FileNotUploadedError
from api.keybords.reply import game_keyboard, user_keyboard

from api.handlers.errors_massages import DONT_GET_PHOTO
from api.google_cloud_storage.gcs_service import GoogleCloudStorageService as GCS
from DB.queries import (
    UserActivity,
    QuestionActivity,
)

user_query = UserActivity()
question_query = QuestionActivity()

user_router = Router()


class ResponsesUser(StatesGroup):
    response_user = State()
    photo = State()
    correct_answer = State()


@user_router.message(Command('start'))
async def get_start(message: Message):
    await message.answer(text='Отлично, давай начнем.', reply_markup=user_keyboard())

    data = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name
    }

    user_query.create_user(data)


@user_router.message(StateFilter(ResponsesUser.response_user))
@user_router.message(F.text == 'Начать игру')
@user_router.message(Command('start_game'))
async def get_photo(message: types.Message, state: FSMContext):
    data_state = await state.get_data()

    if message.text.casefold() != "/start_game" and message.text != 'Начать игру':
        photo: list = data_state.get("photo")

        response = question_query.get_answers_question(photo[0].name)

        if message.text in response:

            if data_state.get('response_user') is None:
                await state.update_data(response_user=[message.text.casefold()])

            else:
                user_responses = data_state.get('response_user')
                user_responses.append(message.text.casefold())

                await state.update_data(response_user=user_responses)

        else:
            await message.answer(text='Выбери из предложенных вариантов!')
            return

        correct_answer = question_query.get_correct_answer(photo_id=photo[0].id, user_answer=message.text)

        if correct_answer:
            data_correct_answer_state = data_state.get('correct_answer')

            if data_correct_answer_state is None:
                await state.update_data(correct_answer=[message.text])

            else:
                data_correct_answer_state.append(correct_answer)

                await state.update_data(correct_answer=data_correct_answer_state)

        file_path = os.path.realpath(photo[0].name)
        os.remove(file_path)

        photo.remove(photo[0])

        await state.set_state(ResponsesUser.photo)
        await state.update_data(photo=photo)

        data_state = await state.get_data()

    if len(data_state) == 0:
        data = question_query.get_photos()

        await state.set_state(ResponsesUser.photo)
        await state.update_data(photo=data)

        data_state = await state.get_data()

    if len(data_state.get('photo')) == 0:

        if data_state.get('correct_answer') is None:
            return await message.answer(text='Я разочарован в тебе', reply_markup=user_keyboard())

        elif len(data_state.get('correct_answer')) == 3:
            await message.answer(text='Да ты шаришь в тачках, лучший!', reply_markup=user_keyboard())

        elif len(data_state.get('correct_answer')) == 2:
            await message.answer(
                text='Неплохо, ты сделал одну ошибку, попробуй пройти игру еще раз!',
                reply_markup=user_keyboard()
            )

        else:
            await message.answer(text='ТЫ бездарь!', reply_markup=user_keyboard())

        await state.clear()

        return

    try:
        photo = data_state.get("photo")

        GCS().get_file(file_name=photo[0].name)

        with open(photo[0].name, 'rb') as file:
            data = file.read()
            photo_path = BufferedInputFile(file=data, filename='post')

            photo: list = data_state.get("photo")

            response = question_query.get_answers_question(photo[0].name)

            reply = game_keyboard(
                text1=response[0],
                text2=response[1],
                text3=response[2],
                text4=response[3],
            )

            await message.answer_photo(photo=photo_path, reply_markup=reply)

            await state.set_state(ResponsesUser.response_user)

    except FileNotUploadedError:
        await message.answer(text='Тех. сбой, я сообщил об этой ошибке разработчикам, скоро это починят')
        return await message.answer(text=DONT_GET_PHOTO)
