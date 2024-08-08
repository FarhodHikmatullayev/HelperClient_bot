from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from loader import db

department_callback_data = CallbackData('department', 'id', 'branch_id')


async def departments_keyboard(*args, branch_id):
    markup = InlineKeyboardMarkup(row_width=1)
    for department_id in args[0]:
        department = await db.select_department(id=department_id)
        text_button = f"{department['name']}".capitalize()
        callback_data = department_callback_data.new(id=department['id'], branch_id=branch_id)
        markup.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=callback_data
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text="⏪ Orqaga",
            callback_data='back_to_branches'
        )
    )

    return markup
