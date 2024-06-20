import asyncpg
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT


async def get_connection():
    conn = await asyncpg.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn


# Функция для создания таблиц при запуске
async def create_tables():
    conn = await get_connection()
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            name TEXT,
            number TEXT,
            location TEXT
        );
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            pr_id SERIAL PRIMARY KEY,
            pr_name TEXT,
            pr_count INTEGER,
            pr_description TEXT,
            pr_price REAL,
            pr_photo TEXT
        );
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            user_id BIGINT,
            user_pr_name TEXT,
            user_pr_count INTEGER,
            total REAL
        );
    ''')
    await conn.close()


# Проверка наличия пользователя в базе данных
async def check_user(user_id):
    conn = await get_connection()
    result = await conn.fetchrow('SELECT 1 FROM users WHERE user_id=$1;', user_id)
    await conn.close()
    return result is not None


# Регистрация нового пользователя
async def register(user_id, name, number, location):
    conn = await get_connection()
    await conn.execute('INSERT INTO users (user_id, name, number, location) VALUES ($1, $2, $3, $4);', user_id, name,
                       number, location)
    await conn.close()


# Получение списка продуктов
async def get_pr():
    conn = await get_connection()
    products = await conn.fetch('SELECT pr_id, pr_name, pr_count FROM products;')
    await conn.close()
    return products


# Получение информации о конкретном продукте
async def get_exact_pr(pr_id):
    conn = await get_connection()
    product = await conn.fetchrow(
        'SELECT pr_name, pr_description, pr_count, pr_price, pr_photo FROM products WHERE pr_id = $1;', pr_id)
    await conn.close()
    return product


# Добавление продукта в корзину
async def add_pr_to_cart(user_id, user_pr, user_pr_count, total):
    conn = await get_connection()
    await conn.execute('INSERT INTO cart (user_id, user_pr_name, user_pr_count, total) VALUES ($1, $2, $3, $4);',
                       user_id, user_pr, user_pr_count, total)
    await conn.close()


# Добавление нового продукта (для админа)
async def add_pr(pr_name, pr_description, pr_count, pr_price, pr_photo):
    conn = await get_connection()
    await conn.execute(
        'INSERT INTO products (pr_name, pr_description, pr_count, pr_price, pr_photo) VALUES ($1, $2, $3, $4, $5);',
        pr_name, pr_description, pr_count, pr_price, pr_photo)
    await conn.close()


# Удаление продукта (для админа)
async def del_pr(pr_id):
    conn = await get_connection()
    await conn.execute('DELETE FROM products WHERE pr_id=$1;', pr_id)
    await conn.close()


# Изменение количества продукта (для админа)
async def change_pr_count(pr_id, new_count):
    conn = await get_connection()
    current_count = await conn.fetchval('SELECT pr_count FROM products WHERE pr_id=$1;', pr_id)
    await conn.execute('UPDATE products SET pr_count=$1 WHERE pr_id=$2;', current_count + new_count, pr_id)
    await conn.close()


# Проверка наличия продуктов
async def pr_check():
    conn = await get_connection()
    result = await conn.fetchrow('SELECT 1 FROM products;')
    await conn.close()
    return result is not None


# Показать корзину пользователя
async def show_cart(user_id):
    conn = await get_connection()
    cart = await conn.fetch('SELECT * FROM cart WHERE user_id=$1;', user_id)
    await conn.close()
    return cart


# Очистить корзину пользователя
async def clear_cart(user_id):
    conn = await get_connection()
    await conn.execute('DELETE FROM cart WHERE user_id=$1;', user_id)
    await conn.close()


# Оформление заказа
async def make_order(user_id):
    conn = await get_connection()
    pr_name = await conn.fetchval('SELECT user_pr_name FROM cart WHERE user_id=$1;', user_id)
    user_pr_count = await conn.fetchval('SELECT user_pr_count FROM cart WHERE user_id=$1;', user_id)
    current_count = await conn.fetchval('SELECT pr_count FROM products WHERE pr_name=$1;', pr_name)

    await conn.execute('UPDATE products SET pr_count=$1 WHERE pr_name=$2;', current_count - user_pr_count, pr_name)

    info = await conn.fetchrow('SELECT * FROM cart WHERE user_id=$1;', user_id)
    address = await conn.fetchval('SELECT location FROM users WHERE user_id=$1;', user_id)

    await conn.close()
    return info, address
