from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType

from data.config import ADMINS
from keyboards.default.menu import back_menu_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, bot, db
from photograph import video_link, photo_link
from states.send_message import SendMessageState


@dp.message_handler(Command('send_message'), user_id=ADMINS, state='*')
async def download_emp(message: types.Message, state: FSMContext):
    text = "Xabar, rasm yoki video jo'natishingiz mumkin"
    await message.answer(text=text, reply_markup=back_menu_keyboard)
    await SendMessageState.content.set()


@dp.message_handler(content_types=ContentType.ANY, state=SendMessageState.content)
async def get_content(message: types.Message, state: FSMContext):
    content_type = message.content_type
    print('content_type', content_type)
    if content_type == 'photo':
        photo = message.photo[-1]
        text = await photo_link(photo)
    elif content_type == 'video':
        video = message.video
        text = await video_link(video)
    elif content_type == 'text':
        text = message.text
    else:
        text = "Siz Rasm, Text, Video jo'nata olasiz\n" \
               "Iltimos qayta urunib ko'ring va yuqoridagilardan birini jo'nating"
        await message.answer(text=text, reply_markup=back_menu_keyboard)
        return

    await state.update_data(
        {
            "content": text
        }
    )
    await message.answer(text="Jo'natilsinmi?", reply_markup=confirm_keyboard)


@dp.callback_query_handler(text='ok', state=SendMessageState.content)
async def confirm_sending_message(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    content = data.get('content')

    users = await db.select_all_users()
    for user in users:
        await bot.send_message(chat_id=user['telegram_id'], text=content)

    text = "Jo'natildi"
    await call.message.answer(text=text, reply_markup=back_menu_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='cancel', state=SendMessageState.content)
async def confirm_sending_message(call: types.CallbackQuery, state: FSMContext):
    text = "Xabar yuborish rad etildi"
    await call.message.answer(text=text, reply_markup=back_menu_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()
