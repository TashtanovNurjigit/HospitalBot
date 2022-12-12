import sqlite3 as sq


# Запуск DB
def sql_start():
    global base, cursor
    base = sq.connect('Hospital')
    cursor = base.cursor()
    if base:
        print('Data Base connected!')
        base.execute(
            '''
            CREATE TABLE IF NOT EXISTS doctors(
                id_doctor INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                photo TEXT
                )
            '''
        )
        base.execute(
            '''
            CREATE TABLE IF NOT EXISTS appointment(
                id_applications INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                date TEXT,
                time TEXT,
                doctor_id INTEGER
                )
            '''
        )
        base.commit()


# Добавление новых значений в DB
async def sql_add_commands(state, table):
    query = None
    if table == 'doctors':
        query = f'INSERT INTO {table} VALUES (?, ?, ?)'
    elif table == 'appointment':
        query = f'INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?)'
    async with state.proxy() as data:
        cursor.execute(query, (None, *tuple(data.values())))
        base.commit()


# Получаем все элементы из таблицы 'appointment'
async def sql_get_all_appointment(message):
    query = f'SELECT * FROM appointment'
    for ret in cursor.execute(query).fetchall():
        doctor = cursor.execute(f'SELECT name FROM doctors WHERE id_doctor = ?', ret[-1])
        await message.answer(f'{ret[1]}\n'
                             f'{ret[2]}\n'
                             f'{ret[3]}\n'
                             f'{ret[4]}\n'
                             f'{doctor}')
        base.commit()


# Получаем записи определенного врача
async def sql_get_doctor_appointment(data, message):
    name_doctor = cursor.execute('SELECT id_doctor FROM doctors WHERE name = ?', (data, )).fetchone()
    for ret in cursor.execute(f'SELECT * FROM appointment WHERE doctor_id = ?', (list(name_doctor)[0], )):
        await message.answer(f'{ret[1]}\n'
                             f'{ret[2]}\n'
                             f'{ret[3]}\n'
                             f'{ret[4]}\n'
                             f'{data}')


async def delete(data, table):
    cursor.execute(f'DELETE FROM {table} WHERE name = ?', (data,))
    base.commit()
