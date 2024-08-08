# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#
# keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
#                                keyboard=[
#                                    [
#                                        KeyboardButton(text="📱",
#                                                       request_contact=True)
#                                    ]
#                                ])

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                               keyboard=[
                                   [
                                       KeyboardButton(text="📱",
                                                      request_contact=True)
                                   ]
                               ])
