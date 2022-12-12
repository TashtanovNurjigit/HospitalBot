from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message
from aiogram import Dispatcher

from DB import sqlite3


class FSMAdmin(StatesGroup):
    name = State()
    photo = State()


async def add_doctors(message: Message):
    await FSMAdmin.name.set()
    await message.reply('Как зовут нового врача?', reply_markup=ReplyKeyboardRemove())


async def load_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Отправьте фото нового врача')


async def load_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await sqlite3.sql_add_commands(state, 'doctors')
    await message.reply('Мы сохранили в базу нового врача!')
    await state.finish()


def register_admin_states(dp: Dispatcher):
    dp.register_message_handler(add_doctors, commands=['new_doctors'], state=None)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_photo,content_types=['photo'], state=FSMAdmin.photo)

