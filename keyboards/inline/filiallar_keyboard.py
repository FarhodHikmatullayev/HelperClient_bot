from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from loader import db

branch_callback_data = CallbackData('filial', 'id')


async def branches_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    branches = await db.select_all_branches()
    for branch in branches:
        text_button = f"{branch['name']}".capitalize()
        callback_data = branch_callback_data.new(id=branch['id'])
        markup.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=callback_data
            )
        )

    return markup
