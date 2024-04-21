from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def game_keyboard(text1: str, text2: str, text3: str, text4: str):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=text1),
            KeyboardButton(text=text2),
        ],
        [
            KeyboardButton(text=text3),
            KeyboardButton(text=text4),
        ]
    ], one_time_keyboard=True)

    return keyboard


def admin_keyboard():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Посмотреть кол-во юзеров')
        ],
        [
            KeyboardButton(text='Добавить новую машину')
        ],
        [
            KeyboardButton(text='Редактировать существующие машины')
        ]
    ], one_time_keyboard=True, resize_keyboard=True)

    return keyboard


def answer_keyboard(data: list):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=data[0]),
            KeyboardButton(text=data[1]),
        ],
        [
            KeyboardButton(text=data[2]),
            KeyboardButton(text=data[3]),
        ]
    ], one_time_keyboard=True)

    return keyboard
