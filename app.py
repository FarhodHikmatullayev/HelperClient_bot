from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_users()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    # await on_startup_notify(dispatcher)


# if __name__ == '__main__':
#     executor.start_polling(dp, on_startup=on_startup, skip_updates=True)


def main():
    # Oxirgi yangilanish ID raqamini olish
    update_offset = 0

    while True:
        try:
            updates = await dp.bot.get_updates(offset=update_offset, timeout=20)
            if updates:
                update_offset = updates[-1].update_id + 1
                await dp.process_updates(updates)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
    main()
