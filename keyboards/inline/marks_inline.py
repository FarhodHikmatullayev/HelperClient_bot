from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from loader import db

mark_callback_data = CallbackData('comment', 'mark')
marks_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='1️⃣',
                callback_data=mark_callback_data.new(mark=1)
            ),
            InlineKeyboardButton(
                text='2️⃣',
                callback_data=mark_callback_data.new(mark=2)
            ),
            InlineKeyboardButton(
                text='3️⃣',
                callback_data=mark_callback_data.new(mark=3)
            ),
            InlineKeyboardButton(
                text='4️⃣',
                callback_data=mark_callback_data.new(mark=4)
            ),
            InlineKeyboardButton(
                text='5️⃣',
                callback_data=mark_callback_data.new(mark=5)
            ),
        ]
    ]
)
