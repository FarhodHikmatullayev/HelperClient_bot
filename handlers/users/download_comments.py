import datetime
import tempfile
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
import openpyxl
import os

from data.config import ADMINS
from keyboards.default.menu import back_menu_keyboard
from loader import dp, db, bot


async def download_all_comments_function():
    comments = await db.select_all_comments()
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    worksheet['A1'] = 'T/r'
    worksheet['B1'] = 'F.I.SH'
    worksheet['C1'] = 'USERNAME'
    worksheet['D1'] = 'TELEFON RAQAM'
    worksheet['E1'] = 'TELEGRAM ID'
    worksheet['F1'] = 'FILIAL NOMI'
    worksheet['G1'] = 'BAHO'
    worksheet['H1'] = 'VAQT'
    worksheet['I1'] = 'FIKR'

    worksheet.cell(row=1, column=1, value='№')
    worksheet.cell(row=1, column=2, value='F.I.SH')
    worksheet.cell(row=1, column=3, value="USERNAME")
    worksheet.cell(row=1, column=4, value='TELEFON RAQAM')
    worksheet.cell(row=1, column=5, value='TELEGRAM ID')
    worksheet.cell(row=1, column=6, value='FILIAL NOMI')
    worksheet.cell(row=1, column=7, value='XODIM ID RAQAMI')
    worksheet.cell(row=1, column=8, value='BAHO')
    worksheet.cell(row=1, column=9, value='VAQT')
    worksheet.cell(row=1, column=10, value='FIKR')
    tr = 0
    for row, comment in enumerate(comments, start=2):
        filial_id = comment['branch_id']
        department_id = comment['department_id']
        if department_id:
            department = await db.select_department(id=department_id)
            department_name = department['name']

        user_id = comment['user_id']

        branch = await db.select_branch(id=filial_id)
        users = await db.select_users(id=user_id)
        user = users[0]

        branch_name = branch['name']
        full_name = user['full_name']
        username = user['username']
        phone = user['phone']
        telegram_id = user['telegram_id']

        tr += 1
        worksheet.cell(row=row, column=1, value=tr)
        worksheet.cell(row=row, column=2, value=full_name)
        worksheet.cell(row=row, column=3, value=username)
        worksheet.cell(row=row, column=4, value=phone)
        worksheet.cell(row=row, column=5, value=telegram_id)
        worksheet.cell(row=row, column=6, value=branch_name)
        worksheet.cell(row=row, column=7, value=comment['employee_code'])
        worksheet.cell(row=row, column=8, value=comment['mark'])
        worksheet.cell(row=row, column=9,
                       value=(comment['created_at'] + datetime.timedelta(hours=5)).strftime('%d.%m.%Y %H:%M'))
        worksheet.cell(row=row, column=10, value=comment['message'])

    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, 'Comments_data.xlsx')
    workbook.save(file_path)

    return temp_dir


@dp.message_handler(Command('download_all_comments'), user_id=ADMINS, state='*')
async def download_emp(message: Message, state: FSMContext):
    await state.finish()
    temp_dir = await download_all_comments_function()

    with open(os.path.join(temp_dir, 'Comments_data.xlsx'), 'rb') as file:
        await message.answer_document(document=file)
        # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    os.remove(os.path.join(temp_dir, 'Comments_data.xlsx'))


@dp.message_handler(Command('download_all_comments'), state='*')
async def download_emp(message: Message, state: FSMContext):
    await state.finish()
    text = "Bu komanda faqat adminlar uchun"
    await message.answer(text=text, reply_markup=back_menu_keyboard)
