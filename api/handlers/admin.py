import os
from aiogram import F, Router, types

from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from api.filters.chat_types import IsAdmin
from api.keybords.reply import admin_keyboard, answer_keyboard

from DB.queries import UserActivity

admin_router = Router()
admin_router.message.filter(IsAdmin())

user_query = UserActivity()


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
    await state.update_data(answer=[message.text.upper()])

    await message.answer(text='Good')
