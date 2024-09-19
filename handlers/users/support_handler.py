from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import back_menu_keyboard
from loader import dp, bot


@dp.message_handler(Command('support'), state='*')
async def support(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    text = "Bot haqida to'liq ma'lumot olish hamda talab va takliflar uchun bizga bog'laning: \n\n" \
           "Tel: +998900832345\n" \
           "Command: /help\n" \
           "Telegram: https://t.me/pydev8747\n" \
           "Pochta manzili: farhodjonhikmatullayev@gmail.com\n" \
           "\n" \
           "Yuqoridagilardan biri orqali murojaat qiling"
    await message.answer(text=text, reply_markup=back_menu_keyboard)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
