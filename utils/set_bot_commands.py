from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("operate_random", "Random funksiyasini ishlatish. Super adminlar uchun"),
            types.BotCommand("download_employees", "Xodimlarni Excel shaklida yuklab olish. Adminlar uchun"),
            types.BotCommand("upload_employees", "Xodimlarni Excel shaklida botga yuklash. Adminlar uchun"),
            types.BotCommand("download_all_promo_codes", "Promocodlarni yuklab olish. Adminlar uchun"),
            types.BotCommand("download_all_comments", "Mijozlarning fikrlarini yuklab olish. Adminlar uchun"),
        ]
    )
