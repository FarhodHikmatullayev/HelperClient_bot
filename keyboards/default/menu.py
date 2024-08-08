from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_menu_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="◀ Bosh Menyu")
        ]
    ]
)
