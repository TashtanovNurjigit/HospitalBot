from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config.config import bot
from DB import sqlite3
from keyboards.cb_keyboards import kb_client
# from data_base import sqlite3_db


# Отвечаем на команды "start, help"
async def start(message: types.Message):
    await message.answer('Выберите действие', reply_markup=kb_client)


# Получаем всех докторов из DB
async def get_doctors(message: types.Message):
    for obj in sqlite3.cursor.execute(f'SELECT * FROM doctors').fetchall():
        await bot.send_photo(message.from_user.id, obj[-1], f'{obj[1]}\n', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('appointment', callback_data=f'appointment_{obj[1]}')))


# Получаем все записи врача
async def get_appointment(call: types.CallbackQuery):
    await sqlite3.sql_get_doctor_appointment(call.data.replace("appointment_", ""), call.message)


# Команда для отмены машинного состояния
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ok')


# Регистрируем все хэндлеры клиента
def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(get_doctors, commands=['doctors'])
    dp.register_callback_query_handler(get_appointment, lambda x: x.data and x.data.startswith('appointment_'))
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

