import os
import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import ADMINS, SUPERADMINS
from handlers.users.download_promocodes import download_all_promo_codes
from keyboards.default.menu import back_menu_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot


@dp.message_handler(Command('operate_random'), user_id=SUPERADMINS, state='*')
async def begin_random(message: types.Message, state: FSMContext):
    await state.finish()
    # download promocodes
    temp_dir = await download_all_promo_codes()

    with open(os.path.join(temp_dir, 'Promo_codes_data.xlsx'), 'rb') as file:
        await message.answer_document(document=file)
        # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    os.remove(os.path.join(temp_dir, 'Promo_codes_data.xlsx'))

    promo_codes = await db.select_all_promo_codes()
    if promo_codes:
        codes = []
        for promo_code in promo_codes:
            code = promo_code['promocode']
            user_id = promo_code['user_id']
            code = {
                'promocode': code,
                'user_id': user_id
            }
            codes.append(code)

        random_code = random.choice(codes)
        selected_code = random_code['promocode']
        selected_user_id = random_code['user_id']
        print('user_id_type', type(selected_user_id))
        user = await db.select_user(id=selected_user_id)
        try:
            user = user[0]
        except:
            pass
        user_username = user['username']
        full_name = user['full_name']
        phone = user['phone']
        telegram_id = user['telegram_id']

        await message.answer(f"Random promo code: '{selected_code}'\n"
                             f"Promocode egasi: {full_name.capitalize()}\n"
                             f"Username: {user_username}\n"
                             f"Phone: {phone}\n"
                             f"Telegram ID: {telegram_id}\n",
                             reply_markup=back_menu_keyboard
                             )
        await message.answer(
            text="Promo kodlarni o'chirishni xohlaysizmi",
            reply_markup=confirm_keyboard
        )
    else:
        text = "Hali bazada foydalanuvchilar promo kodlari saqlanmagan.\n" \
               "Yoki o'yin hali o'tkazilmagan bo'lishi mumkin"
        await message.answer(
            text=text,
            reply_markup=back_menu_keyboard
        )


@dp.message_handler(Command('operate_random'), state='*')
async def begin_random(message: types.Message, state: FSMContext):
    text = "Bu komanda faqat SUPER adminlar uchun"
    await message.answer(text=text, reply_markup=back_menu_keyboard)


@dp.callback_query_handler(text="ok")
async def delete_promo_codes(call: types.CallbackQuery):
    await db.delete_all_promocodes()
    text = "Barcha promo_codlar o'chirildi"
    await call.message.answer(
        text=text,
        reply_markup=back_menu_keyboard
    )
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text='cancel')
async def cancel_prom_code(call: types.CallbackQuery):
    text = "Siz promo_codlarni o'chirishni bekor qildingiz"
    await call.message.answer(
        text=text,
        reply_markup=back_menu_keyboard
    )
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
