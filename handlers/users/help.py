from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ""
    text += "Buyruqlar: \n" \
            "/start - Botni ishga tushirish \n" \
            "/help - Yordam \n" \
            "\n" \
            "Botning maqsadi: Maqsad"
    # text = ("Buyruqlar: ",
    #         "/start - Botni ishga tushirish",
    #         "/help - Yordam")
    
    await message.answer(text=text)
