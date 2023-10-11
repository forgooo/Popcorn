import telebot
from telebot import types

from Menu.Menu_arry import menu_info, typ, photo, size, prices, size_to_price
from bd.info_bd import *
from list.orders import *

db = DB()
bot = telebot.TeleBot('5382164610:AAGvlx54ZTPYIryxFHwR3Cf1yIpbetrSIyc')

ch = False


@bot.message_handler(commands=['start'])
def start_message(message):
    text = 'Здравствуйте'
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, 'Что вы хотели?')
    main_chose(message)


def main_chose(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Заказать")
    markup.add(item1)
    item1 = types.KeyboardButton("Мои заказы")
    markup.add(item1)
    item1 = types.KeyboardButton("Меню")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Чем я могу вам помочь:', reply_markup=markup)
    bot.register_next_step_handler(message, message_reply)


def Yes_No_choose(message, question, function, answers):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(answers[0])
    markup.add(item1)
    item1 = types.KeyboardButton(answers[1])
    markup.add(item1)
    bot.send_message(message.chat.id, question, reply_markup=markup)
    bot.register_next_step_handler(message, function)


@bot.message_handler(commands=['text'])
def message_reply(message):
    if message.text == "Меню":
        menu_shower(message.from_user.id, message)
    elif message.text == "Заказать":
        order(message.from_user.id, message)
    elif message.text == 'Мои заказы':
        my_order(message)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод')
        bot.register_next_step_handler(message, message_reply)


def my_order(message):
    bot.send_message(message.from_user.id, 'Тут пока пусто')
    main_chose(message)


def menu_shower(chat_id, message):
    bot.send_message(chat_id, 'Мы можем предложить вам:')
    data = menu_info(typ)
    photos = menu_info(photo)
    for i in range(1, len(data), 2):
        reqwest = ''
        reqwest += '' + data[i - 1] + ''
        reqwest += '-------------------------\n'

        reqwest += data[i]
        bot.send_photo(chat_id, photo=photos[(i // 2) - 1], caption=reqwest)
    for i in photos:
        i.close()
    bot.send_message(chat_id, 'Это конец нашего меню')
    main_chose(message)


address = ''
time = ''
basket = []
order_flag = False


def order(chat_id, message):
    bot.send_message(chat_id, 'Мы можем предложить вам:')
    data = menu_info(typ)
    photos = menu_info(photo)
    reqwest = ''
    global order_flag
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if order_flag:
        button = (types.InlineKeyboardButton(text='Открыть корзину'))
    else:
        button = (types.InlineKeyboardButton(text='Отменить'))
    markup.add(button)
    for i in range(1, len(data), 2):
        button = (types.InlineKeyboardButton(text=(data[i - 1])))
        markup.add(button)
        reqwest = ''
        reqwest += '' + data[i - 1] + ''
        reqwest += '-------------------------\n'

        reqwest += data[i]
        bot.send_photo(chat_id, photo=photos[(i // 2) - 1], caption=reqwest, reply_markup=markup)
    for i in photos:
        i.close()
    bot.register_next_step_handler(message, order_maker)


# variable
type_of_order = ''
size_order = 1
count_of_order = 0
user_id = 0
basket_name_item = []
basket_price_item = []
basket_count_item = []
basket_size_item = []


@bot.message_handler(commands=['text'])
def order_maker(message):
    if message.text == 'Отменить':
        bot.send_message(message.from_user.id, 'Хорошо')
        main_chose(message)
    elif message.text == 'Открыть корзину':
        in_basket(message)
    elif (message.text + '\n') in menu_info(typ):
        for i in range(len(menu_info(typ))):
            if (message.text + '\n') == menu_info(typ)[i]:
                basket_name_item.append(i / 2 + 1)
        global type_of_order
        type_of_order = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = []
        size_data = menu_info(size)
        for i in size_data:
            button.append(types.InlineKeyboardButton(text=i))
        markup.add(*button)
        bot.send_message(message.from_user.id, 'Выберите размер', reply_markup=markup)
        global size_order
        size_order = ''
        bot.register_next_step_handler(message, size_choose)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод')
        bot.register_next_step_handler(message, message_reply)


@bot.message_handler(commands=['text'])
def size_choose(message):
    global size_order
    if message.text in menu_info(size):
        size_order = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(1, 11, 3):
            button = []
            for j in range(i, i + 3):
                button.append(types.InlineKeyboardButton(text=(str(j))))
            markup.add(*button)
        bot.send_message(message.from_user.id, 'Выберите количество', reply_markup=markup)
        bot.register_next_step_handler(message, cout_order)
    else:
        bot.send_message(message.from_user.id, 'Некорректный размер')
        bot.register_next_step_handler(message, size_choose)


@bot.message_handler(commands=['text'])
def cout_order(message):
    global count_of_order
    if is_num(message.text):
        count_of_order = int(message.text)
        bot.send_message(message.from_user.id, 'Давайте проверим:')
        bot.send_message(message.from_user.id,
                         'Попкорн ' + type_of_order + '\nРазмер ' + str(size_order) + '\nКоличество ' + str(
                             count_of_order))
        Yes_No_choose(message, 'Куда дальше?', end_order, ('Добавить позицию в корзину\nи вернуться к меню', 'Отмена'))
    else:
        bot.send_message(message.from_user.id, 'Введите число')
        bot.register_next_step_handler(message, cout_order)


def is_num(a):
    try:
        int(a)
        return True
    except ValueError:
        return False


@bot.message_handler(commands=['text'])
def end_order(message):
    if message.text == 'Добавить позицию в корзину\nи вернуться к меню':
        global order_flag
        order_flag = True
        global basket
        global basket_count_item
        global basket_size_item
        global basket_price_item
        basket.append([type_of_order, size_order, count_of_order])
        basket_count_item.append(count_of_order)
        for i in range(len(size())):
            if size_order == size()[i]:
                basket_size_item.append(i + 1)
        basket_price_item.append(size_to_price(basket_name_item[-1], basket_size_item[-1]))
        order(message.from_user.id, message)
    elif message.text == 'Отмена':
        order(message.from_user.id, message)


def in_basket(message):
    bot.send_message(message.from_user.id, 'Ваш заказ')
    request = ''
    global basket
    print(basket)
    for i in range(len(basket)):
        request += str(i + 1) + '.\nПопкорн ' + basket[i][0] + '\nРазмер ' + basket[i][1] + '\nКоличество ' + str(
            basket[i][2]) + '\n\n'

    if request == '':
        bot.send_message(message.from_user.id, 'Пуст')
        main_chose(message)
    else:
        bot.send_message(message.from_user.id, request)
        Yes_No_choose(message, 'Всё верно?', send_order_to_bd_or_not,
                      ('Да, давайте продолжим', 'Нет, я хочу изменить заказ'))


@bot.message_handler(commands=['text'])
def send_order_to_bd_or_not(message):
    if message.text == 'Да, давайте продолжим':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.InlineKeyboardButton('Вернуться')
        markup.add(button)
        bot.send_message(message.from_user.id, 'Введите адрес достваки', reply_markup=markup)
        bot.register_next_step_handler(message, last_step)
    elif message.text == 'Нет, я хочу изменить заказ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(0, len(basket), 3):
            button = []
            for j in range(i, i + 3):
                button.append(types.InlineKeyboardButton(text=(str(j + 1))))
                if len(basket) - 1 == j:
                    break
            markup.add(*button)

        button = types.InlineKeyboardButton(text='Я хочу добавить ещё одну позицию')
        markup.add(button)

        bot.send_message(message.from_user.id, 'Какую позицию вы хотите изменить?', reply_markup=markup)
        bot.register_next_step_handler(message, change_position)

    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод')
        bot.register_next_step_handler(message, send_order_to_bd_or_not)


index_position = 0


@bot.message_handler(commands=['text'])
def change_position(message):
    if is_num(message.text):
        if 1 <= int(message.text) <= len(basket):
            global index_position
            index_position = int(message.text) - 1
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = (types.InlineKeyboardButton('Размер'))
            markup.add(button)
            button = (types.InlineKeyboardButton('Количество'))
            markup.add(button)
            button = (types.InlineKeyboardButton('Удалить позицию'))
            markup.add(button)
            button = (types.InlineKeyboardButton('Отмена'))
            markup.add(button)
            bot.send_message(message.from_user.id, 'Что вы хотите изменить?', reply_markup=markup)
            bot.register_next_step_handler(message, change_position_choose)
        else:
            bot.send_message(message.from_user.id, 'Некорректный ввод')
            bot.register_next_step_handler(message, change_position)
    elif message.text == "Я хочу добавить ещё одну позицию":
        order(message.from_user.id, message)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод')
        bot.register_next_step_handler(message, change_position)


@bot.message_handler(commands=['text'])
def change_position_choose(message):
    global basket_name_item
    global basket_size_item
    global basket_price_item
    global basket_count_item
    if message.text == 'Удалить позицию':
        basket_name_item.pop(index_position)
        basket_size_item.pop(index_position)
        basket_price_item.pop(index_position)
        basket_count_item.pop(index_position)
        basket.pop(index_position)
        in_basket(message)
    elif message.text == 'Количество':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(1, 11, 3):
            button = []
            for j in range(i, i + 3):
                button.append(types.InlineKeyboardButton(text=(str(j))))
            markup.add(*button)
        bot.send_message(message.from_user.id, 'Выберите количество', reply_markup=markup)
        bot.register_next_step_handler(message, replace_count)
    elif message.text == 'Отмена':
        in_basket(message)
    elif message.text == 'Размер':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = []
        size_data = menu_info(size)
        for i in size_data:
            button.append(types.InlineKeyboardButton(text=i))
        markup.add(*button)
        bot.send_message(message.from_user.id, 'Выберите размер', reply_markup=markup)
        bot.register_next_step_handler(message, replace_size)


@bot.message_handler(commands=['text'])
def replace_count(message):
    if is_num(message.text):
        basket[index_position][2] = int(message.text)

        global basket_count_item
        basket_count_item[index_position] = int(message.text)

        in_basket(message)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод')
        bot.register_next_step_handler(message, replace_count)


@bot.message_handler(commands=['text'])
def replace_size(message):
    size_data = menu_info(size)
    if message.text in size_data:
        basket[index_position][1] = (message.text)

        global basket_size_item
        for i in range(len(size())):
            if size_order == size()[i]:
                basket_size_item[index_position] = i + 1

        in_basket(message)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод')
        bot.register_next_step_handler(message, replace_size)


@bot.message_handler(commands=['text'])
def last_step(message):
    global basket
    global order_flag
    if message.text == "Вернуться":
        in_basket(message)
    elif True:
        global user_id
        user_id = message.chat.id
        for i in range(len(basket_name_item)):
            db.add_to_db(int(get_user_id()), int(get_deliver_id()), int(get_food_id()[i]), int(get_count()[i]),
                         int(get_food_size()[i]), int(get_price()[i]), get_address(), check_status())

        bot.send_message(message.from_user.id, 'Спасибо за заказ! Ожидайте свой попкорн в зоне доставки')
        basket.clear()
        order_flag = False
        main_chose(message)
    elif message.text not in info_bd(street_bd):
        bot.send_message(message.from_user.id, 'К сожалению вы не входите в нашу зону доставки')
        basket.clear()
        order_flag = False
        main_chose(message)


def get_user_id():
    global user_id
    return user_id


def get_food_id():
    global basket_name_item
    return basket_name_item


def get_deliver_id():
    return 0


def get_count():
    global basket_count_item
    return basket_count_item


def get_food_size():
    global basket_size_item
    return basket_size_item


def get_price():
    global basket_price_item
    return basket_price_item


def get_address():
    global address
    return address


def check_status():
    return False


bot.polling(none_stop=True, interval=0)
