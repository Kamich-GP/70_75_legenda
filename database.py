# Работа с БД
import sqlite3

# Подключение к БД
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Python + SQL
sql = connection.cursor()

# Создание таблиц
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(tg_id INTEGER, name TEXT, num TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT, pr_des TEXT, pr_count INTEGER, '
            'pr_price INTEGER, pr_photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS cart '
            '(tg_id INTEGER, user_product TEXT, user_pr_amount INTEGER);')

## Методы пользователя ##
# Регистрация
def register(tg_id, name, num):
    sql.execute('INSERT INTO users VALUES (?, ?, ?);', (tg_id, name, num))
    # Фиксируем изменения
    connection.commit()

# Проверка на наличие в БД
def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE tg_id=?;', (tg_id,)).fetchone():
        return True
    else:
        return False

## Методы продуктов ##
# Вывод всего из таблицы продуктов
def get_all_pr():
    return sql.execute('SELECT * FROM products;').fetchall()

# Вывод товаров под кнопки
def get_pr_buttons():
    return [i[:2] for i in get_all_pr() if i[3] > 0]

# Вывод определенного товара
def get_exact_pr(pr_id):
    return sql.execute('SELECT * FROM products WHERE pr_id=?;', (pr_id,)).fetchone()

# Вывод цены товара по названию
def get_pr_price(pr_name):
    return sql.execute('SELECT pr_price FROM products WHERE pr_name=?;', (pr_name,)).fetchone()[0]

## Методы корзины ##
# Добавление в корзину
def add_to_cart(tg_id, user_product, user_pr_amount):
    sql.execute('INSERT INTO cart VALUES (?, ?, ?);', (tg_id, user_product, user_pr_amount))
    # Фиксируем изменения
    connection.commit()

# Очистка корзины
def clear_cart(tg_id):
    sql.execute('DELETE FROM cart WHERE tg_id=?;', (tg_id,))
    # Фиксируем изменения
    connection.commit()

# Вывод корзины
def show_cart(tg_id):
    return sql.execute('SELECT * FROM cart WHERE tg_id=?;', (tg_id,)).fetchall()

# Оформление заказа
def make_order(tg_id):
    user_cart = [i[1:] for i in show_cart(tg_id)]

    for user_product, product_count in user_cart:
        # Достаем кол-во товара со СКЛАДА
        stock = sql.execute('SELECT pr_count FROM products WHERE pr_name=?;', (user_product,)).fetchone()[0]
        new_count = stock - product_count
        sql.execute('UPDATE products SET pr_count=? WHERE pr_name=?;', (new_count, user_product))
    # Фиксируем изменения
    connection.commit()

## Методы администратора ##
# Добавление товара в БД
def add_pr_to_db(pr_name, pr_des, pr_count, pr_price, pr_photo):
    sql.execute('INSERT INTO products (pr_name, pr_des, pr_count, pr_price, pr_photo) '
                'VALUES (?, ?, ?, ?, ?);', (pr_name, pr_des, pr_count, pr_price, pr_photo))
    # Фиксируем изменения
    connection.commit()
