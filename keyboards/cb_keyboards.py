from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton('/new_appointment')
b2 = KeyboardButton('/doctors')
b3 = KeyboardButton('/admin')


kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b1).insert(b2)
kb_client.add(b3)