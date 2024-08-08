from aiogram import types

from keyboards.inline.filiallar_keyboard import branches_keyboard
from loader import dp, bot


@dp.message_handler(text='◀ Bosh Menyu')
async def back_to_menu(message: types.Message):
    markup = await branches_keyboard()
    await message.answer(text='Quyidagi filiallardan birini tanlang', reply_markup=markup)
