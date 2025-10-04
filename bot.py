# Основная логика бота
import telebot
import buttons
import database

# Создаем объект бота
bot = telebot.TeleBot('TOKEN')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Проверяем, зарегистрировался ли юзер
    if database.check_user(user_id):
        bot.send_message(user_id, 'Добро пожаловать!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию!\n'
                                  'Введите свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)

# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер!',
                     reply_markup=buttons.num_button())
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)

# Этап получения номера
def get_num(message, user_name):
    user_id = message.from_user.id
    # Проверяем правильность отправки номера
    if message.contact:
        user_num = message.contact.phone_number
        # Регистрируем юзера
        database.register(user_id, user_name, user_num)
        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте номер по кнопке!')
        # Возвращение на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)

# Обработчик команды /admin
@bot.message_handler(commands=['admin'])
def admin(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Чтобы добавить товар, впишите следующие данные:\n'
                              'Название, описание, кол-во на складе, цена, фото\n'
                              'Пример:\n'
                              'Картошка фри, свежая и вкусная, 100, 14000, https://fries.jpg\n\n'
                              'Фото загружать на https://postimages.org/ и присылать прямую ссылку!')
    # Переход на этап получения товара
    bot.register_next_step_handler(message, get_pr)


def get_pr(message):
    user_id = message.from_user.id
    product = message.text.split(', ')
    database.add_pr_to_db(*product)
    bot.send_message(user_id, 'Товар успешно добавлен!')

# Запуск бота
bot.polling(non_stop=True)
