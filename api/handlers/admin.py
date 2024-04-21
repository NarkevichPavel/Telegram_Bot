import os
from aiogram import F, Router, types, Bot

from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from api.filters.chat_types import IsAdmin
from api.keybords.reply import admin_keyboard, answer_keyboard

from DB.queries import UserActivity, QuestionActivity
from api.google_cloud_storage.gcs_service import GoogleCloudStorageService

admin_router = Router()
admin_router.message.filter(IsAdmin())

user_query = UserActivity()
question_query = QuestionActivity()

gcs = GoogleCloudStorageService()


class Question(StatesGroup):
    answer = State()
    photo = State()
    correct_answer = State()


@admin_router.message(Command('admin_panel'))
async def admin_panel(message: types.Message):
    reply = admin_keyboard()
    await message.answer(text='Вот доступные действия', reply_markup=reply)


@admin_router.message(F.text.casefold() == 'посмотреть кол-во юзеров')
async def admin_count_users(message: types.Message):
    count = user_query.count_users()
    reply = admin_keyboard()

    await message.answer(text=f'Кол-во активных пользователей: {count}', reply_markup=reply)


@admin_router.message(F.text.casefold() == 'добавить новую машину')
async def create_first_answer(message: types.Message, state: FSMContext):
    await message.answer(text='Введите первый вариант ответа')
    await state.set_state(Question.answer)


@admin_router.message(StateFilter(Question.answer))
async def create_other_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if data.get('answer') is None:
        await state.update_data(answer=[message.text.upper()])

    elif 0 < len(data.get('answer')) <= 2:
        answers = data.get('answer')
        answers.append(message.text.upper())

        await state.update_data(answer=answers)

    elif len(data.get('answer')) == 3:
        answers = data.get('answer')
        answers.append(message.text.upper())

        await state.update_data(answer=answers)

        data = await state.get_data()
        reply = answer_keyboard(data=data.get('answer'))

        await message.answer(text='ВЫберите правильный овтет', reply_markup=reply)
        await state.set_state(Question.correct_answer)
        return

    await message.answer(text='again')
    await state.set_state(Question.answer)


@admin_router.message(StateFilter(Question.correct_answer))
async def create_correct_answer(message: types.Message, state: FSMContext):
    await state.update_data(correct_answer=[message.text.upper()])

    await message.answer(text='Скинь мне фотографию машины')
    await state.set_state(Question.photo)


@admin_router.message(StateFilter(Question.photo))
async def get_photo(message: types.Message, state: FSMContext, bot: Bot):
    if message.photo:
        file_path = str(gcs.get_file_path()) + '/'

        await bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')

        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file_path=file.file_path, destination=f"{file_path}{file.file_id}.png")

        if gcs.create_file(file_name=f"{file.file_id}.png", path=file_path):
            os.remove(file_path + f'{file.file_id}.png')

            data = {'name': f'{file.file_id}.png'}

            await state.update_data(photo=data.get('name'))

            state_data = await state.get_data()
            question_query.create_question(state_data)

            await message.answer(text='Я успешно сохранил фото')

            await state.clear()

    else:
        await message.answer(text='Мне надо фотография!')

        await message.answer(text='Скинь мне фотографию машины')
        await state.set_state(Question.photo)

        return
