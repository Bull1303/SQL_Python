import psycopg2


def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    lastname VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonenumbers(
    number CHAR(11) PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id)
    );
    """)
    # print('Таблицы созданы успешно!')
    return 'Таблицы созданы успешно!'


def delete_db(cur):
    cur.execute("""
        DROP TABLE clients, phonenumbers CASCADE;
        """)
    # print('Таблицы удалены успешно!')
    return 'Таблицы удалены успешно!'


def add_phone(cur, client_id, number):
    cur.execute("""
    INSERT INTO phonenumbers(number, client_id)
    VALUES (%s, %s)
    """, (number, client_id))
    # print(f'Клиенту {client_id} добавлен номер телефона {number}')
    return f'Клиенту {client_id} добавлен номер телефона {number}'


def add_client(cur, name, lastname, email, number=None):
    cur.execute("""
    INSERT INTO clients (name, lastname, email)
    values (%s, %s, %s)
    """, (name, lastname, email))

    cur.execute("""
    SELECT id FROM clients
    ORDER BY id DESC
    LIMIT 1
    """)
    client_id = cur.fetchone()[0]
    if number is None:
        # print(f'Клиент {name, lastname, email} добавлен БЕЗ номера телефона')
        return f'Клиент {name, lastname, email} добавлен БЕЗ номера телефона'
    else:
        add_phone(cur, client_id, number)
        # print(f'Клиент {name, lastname, email} добавлен с номером телефона')
        return f'Клиент {name, lastname, email} добавлен с номером телефона'


def change_client(cur, id, name=None, lastname=None, email=None):
    cur.execute("""
    SELECT * from clients
    WHERE id = %s
    """, (id, ))
    data = cur.fetchone()
    if name is None:
        name = data[1]
    if lastname is None:
        lastname = data[2]
    if email is None:
        email = data[3]
    cur.execute("""
    UPDATE clients
    SET name = %s, lastname = %s, email = %s
    WHERE id = %s
    """, (name, lastname, email, id))
    return 'Данные клиента изменены успешно'


def delete_phone(cur, number):
    cur.execute("""
    DELETE FROM phonenumbers
    WHERE number = %s
    """, (number, ))
    return f'Номер телефона {number} успешно удалён!'


def delete_client(cur, id):
    cur.execute("""
    DELETE FROM phonenumbers
    WHERE client_id = %s
    """, (id, ))
    cur.execute("""
    DELETE FROM clients
    WHERE id = %s
    """, (id, ))
    return f'Клиент номер {id} успешно удалён!'


def find_client(cur, name=None, lastname=None, email=None, number=None):
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if lastname is None:
        surname = '%'
    else:
        surname = '%' + lastname + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if number is None:
        cur.execute("""
             SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
             JOIN phonenumbers p ON c.id = p.client_id
             WHERE c.name LIKE %s AND c.lastname LIKE %s
             AND c.email LIKE %s
             """, (name, surname, email))
    else:
        cur.execute("""
             SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
             LEFT JOIN phonenumbers p ON c.id = p.client_id
             WHERE c.name LIKE %s AND c.lastname LIKE %s
             AND c.email LIKE %s AND p.number like %s
             """, (name, surname, email, number))
    return cur.fetchall()


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        # Удаляем имеющиеся таблицы:
        # print(delete_db(cur))

        # Создаём новые пустые таблицы:
        # print(create_db(cur))

        # Создаём несколько пользователей с номерами телефонов и без:
        # print(add_client(cur, 'Пётр', 'Иванов', 'petr@maill.ru', 79001002233))
        # print(add_client(cur, 'Иван', 'Петров', 'ivan@mail.ru'))
        # print(add_client(cur, 'Василий', 'Сергеев', 'vasil@mail.ru'))
        # print(add_client(cur, 'Сергей', 'Васильев', 'serg@mail.ru', 79115336789))

        # Добавляем пользователю номер телефона:
        # print(add_phone(cur, 1, 79235478590))
        # print(add_phone(cur, 2, 79265906783))

        # Изменяем данные пользователя:
        # print(change_client(cur, 1, 'Владислав', 'Мишин', 'vlad@mail.ru'))

        # Удаляем номер телефона:
        # print(delete_phone(cur, '79001002233'))

        # Удаляем клиента из БД:
        # print(delete_client(cur, 2))

        # Выполняем поиск по БД с разными параметрами:
        # print(find_client(cur, 'Владислав', None, None, None))
        # print(find_client(cur, None, 'Васильев', None, None))
        # print(find_client(cur, None, None, 'ivan@mail.ru', None))
        # print(find_client(cur, None, None, None, '79235478590'))

conn.close()