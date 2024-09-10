import asyncpg
from aiogram import types
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import filters, FSMContext

from keyboards.inline.filiallar_keyboard import branches_keyboard
from loader import dp, db

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.default.contact_button import keyboard
from loader import dp


@dp.message_handler(content_types='contact')
async def get_contact(message: Message):
    contact = message.contact
    print('full_name', message.from_user.full_name)
    try:
        user = await db.create_user(phone=contact.phone_number, telegram_id=message.from_user.id,
                                    username=message.from_user.username, full_name=message.from_user.full_name)
        await message.answer(f"Rahmat, <b>{contact.full_name}</b>.\n"
                             f"Sizning {contact.phone_number} raqamingizni qabul qildik.",
                             reply_markup=ReplyKeyboardRemove())
        markup = await branches_keyboard()
        await message.answer(text="Endi quyidagi filiallardan birini tanlang", reply_markup=markup)
    except asyncpg.exceptions.UniqueViolationError:
        text = "Siz allaqachon ro'yxatdan o'tgan ekansiz\n" \
               "Endi quyidagi filiallardan birini tanlang"
        markup = await branches_keyboard()
        await message.answer(text=text, reply_markup=markup)


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    print('user_telegram_id', message.from_user.id)

    users = await db.select_users(telegram_id=message.from_user.id)
    if not users:
        text = f"Salom, {message.from_user.full_name}!\n"
        text += "Botimizga xush kelibsiz\n" \
                "Fikr bildirish uchun kontaktingizni yuboring"

        await message.answer(text, reply_markup=keyboard)

    else:
        text = f"Salom, {message.from_user.full_name}!\n"
        text += "Botimizga xush kelibsiz\n" \
                "Fikr bildirish uchun filiallardan birini tanlang"
        markup = await branches_keyboard()
        await message.answer(text=text, reply_markup=markup)
    await state.finish()