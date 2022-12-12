from config.config import dp
from aiogram import executor

from DB import sqlite3
from admin import (
    admin_states, admin_handlers)
from handlers.client import register_client_handlers
from handlers.appointment_states import register_states_appointment


# Функция для подключения DB
async def on_startup(_):
    sqlite3.sql_start()
    print('TeleBot')


admin_states.register_admin_states(dp)
admin_handlers.register_admin_handlers(dp)
register_states_appointment(dp)
register_client_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
