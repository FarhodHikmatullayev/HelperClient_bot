from aiogram import executor
import logging
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from keep_alive import keep_alive
from data.config import DEVELOPMENT_MODE, BOT_TOKEN

if not DEVELOPMENT_MODE:
    keep_alive()


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    await db.create()
    # await db.drop_users()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    # await on_startup_notify(dispatcher)


# async def on_shutdown(dispatcher):
#     logging.warning('Shutting down..')
#     await bot.delete_webhook()
#     conn.close()
#     logging.warning('Bye!')


WEBHOOK_HOST = 'https://helperclient-bot.onrender.com'  # 'https://rabid-owl-bot.onrender.com'  # Change this to your server URL
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
