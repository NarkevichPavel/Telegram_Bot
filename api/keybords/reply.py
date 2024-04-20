from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


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
