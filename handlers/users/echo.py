from aiogram import types

from keyboards.inline.filiallar_keyboard import branches_keyboard
from loader import dp


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    text = "Bunday buyruq mavjud emas! \n" \
           "Baho berish uchun quyidagilardan filiallardan birini tanlang"
    markup = await branches_keyboard()

    await message.answer(text, reply_markup=markup)
