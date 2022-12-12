from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config.config import bot, ADMIN
from keyboards.admin_keyboards import kb_admin
from DB import sqlite3


async def admin(message: types.Message):
    if str(message.from_user.id) == ADMIN:
        await message.answer('Выберите действие', reply_markup=kb_admin)
    else:
        await message.answer('Вы не являетесь админом')


async def get_doctors(message: types.Message):
    if str(message.from_user.id) == ADMIN:
        for obj in sqlite3.cursor.execute(f'SELECT * FROM doctors').fetchall():
            print(obj[0])
            await bot.send_photo(message.from_user.id, obj[-1], f'{obj[1]}\n', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('delete', callback_data=f'delete_{obj[1]}')))
    else:
        await message.answer('Вы не являетесь админом')


async def delete(call: types.CallbackQuery):
    await sqlite3.delete(call.data.replace('delete_', ''), 'doctors')
    await call.answer(text=f'{call.data.replace("delete_", "")} удален ', show_alert=True)


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_message_handler(get_doctors, commands=['edit_doctors'])
    dp.register_callback_query_handler(delete, lambda x: x.data and x.data.startswith('delete_'))
