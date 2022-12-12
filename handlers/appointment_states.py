from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.types import (
    CallbackQuery, Message)
from aiogram import Dispatcher

from DB import sqlite3
from config.config import bot, dp


# Создаем класс для машинного состояния
class FSMAppointment(StatesGroup):
    name = State()
    description = State()
    date = State()
    time = State()
    doctor = State()


# Запускаем машинное состояние
async def add_appointment(message: Message):
    await FSMAppointment.name.set()
    await message.reply('Как вас зовут?', reply_markup=ReplyKeyboardRemove())


# Ловим первый ответ и записываем в значение name
async def load_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAppointment.next()
    await message.reply('Что вы хотели проверить у нашего врача?')


# Ловим второй ответ и записываем в значение description
async def load_description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAppointment.next()
    await message.reply('Какого числа вы хотели посетить врача?')


# Ловим третий ответ и записываем в значение date
async def load_date(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await FSMAppointment.next()
    await message.reply('Напишите время посещения')


# Ловим четвертый ответ и записываем в значение time
async def load_time(message: Message, state: FSMContext):
    date, time = None, None
    async with state.proxy() as data:
        data['time'] = message.text
        date = data['date']
        time = data['time']
    if sqlite3.cursor.execute(f'SELECT date FROM appointment WHERE date = ?', (date, )).fetchall() and sqlite3.cursor.execute(f'SELECT time FROM appointment WHERE time = ?', (time, )).fetchall():
        await message.reply('К сожалению в это время имеется запись')
    else:
        await FSMAppointment.next()
        await message.reply(f'Выберете какого врача вы хотели бы посетить\n')
        for obj in sqlite3.cursor.execute('SELECT name FROM doctors').fetchall():
            await message.answer(f'{obj[0]}')


# Ловим последний ответ и записываем в значение doctor и записываем данные в DB
async def load_doctors(message: Message, state: FSMContext):
    message_appointment = None
    async with state.proxy() as data:
        name_doctors = list()
        for obj in sqlite3.cursor.execute('SELECT name FROM doctors').fetchall():
            name_doctors.append(obj[0])
        if message.text in name_doctors:
            for id_doctor in sqlite3.cursor.execute(f'SELECT id_doctor FROM doctors WHERE name = ?', (message.text,)).fetchall():
                data['doctor'] = id_doctor[0]
                await message.answer(f"{data['name']}\n"
                                     f"{data['description']}\n"
                                     f"{data['date']}\n"
                                     f"{data['time']}\n"
                                     f"{message.text}\n"
                                     )
        else:
            await message.reply('К сожалению у нас нет такого врача')
    await sqlite3.sql_add_commands(state, 'appointment')
    await message.reply('Мы записали вас')

    await state.finish()


# Регистрация всех хэндлеров машинного состояния
def register_states_appointment(disp: Dispatcher):
    disp.register_message_handler(add_appointment, commands=['new_appointment'], state=None)
    disp.register_message_handler(load_name, state=FSMAppointment.name)
    disp.register_message_handler(load_description, state=FSMAppointment.description)
    disp.register_message_handler(load_date, state=FSMAppointment.date)
    disp.register_message_handler(load_time, state=FSMAppointment.time)
    disp.register_message_handler(load_doctors, state=FSMAppointment.doctor)

