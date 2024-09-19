from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

department_or_employee_callback_data = CallbackData('check', 'department_or_employee', 'branch_id')


async def check_markup(branch_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Xizmat ko'rsatishga (Xodimga)",
                    callback_data=department_or_employee_callback_data.new(
                        department_or_employee='employee',
                        branch_id=branch_id
                    )
                ),
                InlineKeyboardButton(
                    text="Mahsulotga",
                    callback_data=department_or_employee_callback_data.new(
                        department_or_employee='department',
                        branch_id=branch_id
                    )
                )
            ]
        ]
    )
    return markup
