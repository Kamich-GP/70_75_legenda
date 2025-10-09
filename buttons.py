# Кнопки
from telebot import types

# Кнопка отправки номера
def num_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Отправить свой номер📞',
                                request_contact=True)
    # Добавляем кнопки в пространство
    kb.add(but1)
    return kb

# Кнопки главного меню
def main_menu(products):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    cart = types.InlineKeyboardButton(text='Корзина🛒', callback_data='cart')
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=i[0])
                    for i in products]
    # Добавляем кнопки в пространство
    kb.add(*all_products)
    kb.row(cart)
    return kb

# Кнопки выбора кол-ва товара
def choose_pr_count(pr_count, plus_or_minus='', amount=1):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Создаем сами кнопки
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')
    to_cart = types.InlineKeyboardButton(text='В корзину🛒', callback_data='to_cart')
    # Алгоритм изменения кол-ва
    if plus_or_minus == 'increment':
        if amount < pr_count:
            count = types.InlineKeyboardButton(text=str(amount+1), callback_data=str(amount))
    elif plus_or_minus == 'decrement':
        if 1 < amount:
            count = types.InlineKeyboardButton(text=str(amount-1), callback_data=str(amount))
    # Добавляем кнопки в пространство
    kb.add(minus, count, plus)
    kb.row(back, to_cart)
    return kb

# Кнопки корзины
def cart_buttons():
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    clear = types.InlineKeyboardButton(text='Очистить корзину🗑️', callback_data='clear')
    order = types.InlineKeyboardButton(text='Оформить заказ🧾', callback_data='order')
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')
    # Добавляем кнопки в пространство
    kb.add(clear, order)
    kb.row(back)
    return kb

# Кнопка отправки локации
def loc_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Отправить локацию📍', request_location=True)
    # Добавляем кнопки в пространство
    kb.add(but1)
    return kb
