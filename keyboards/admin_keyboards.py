from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton('/edit_doctors')
b2 = KeyboardButton('/new_doctors')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin.add(b1).insert(b2)
