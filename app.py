from aiogram import executor

from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from keep_alive import keep_alive
from data.config import DEVELOPMENT_MODE

if not DEVELOPMENT_MODE:
    keep_alive()


async def on_startup(dispatcher):
    # await set_webhook()
    await db.create()
    # await db.drop_users()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    # await on_startup_notify(dispatcher)


# this is for webhook
# async def set_webhook():
#     webhook_url = f'https://helperclient-bot.onrender.com/webhook'
#     await bot.set_webhook(webhook_url)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
