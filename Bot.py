from telebot import *
from telebot import types
from Token import token as t
import sqlite3
from NeuralNetWork import NeuralNetWork as NNW
from graph_buider import graph_builder

start = False
bot = telebot.TeleBot(t)
con = sqlite3.connect('DataBase.db')
cur = con.cursor()
USERS = [i[0] for i in cur.execute('''SELECT telegram_id FROM Users''').fetchall()]
info = cur.execute(f'''SELECT * FROM Dishes''').fetchall()
dishes = []
categorys = []
ids_in_count = []
for i in info:
    dishes.append(i[0])
    categorys.append(i[1])
    ids_in_count.append(i[2])
categorys = list(set(categorys))
counts = cur.execute(f'''SELECT * FROM Count''').fetchall()


# dishes = [i[0] for i in cur.execute(f"""SELECT Dish FROM Dishes""").fetchall()]
# categorys, ids_in_count = [], []
# for i in dishes:
#     categorys.append([j[0] for j in cur.execute(f'''SELECT Category FROM Dishes WHERE Dish = "{i}"''').fetchall()])
#     ids_in_count.append([j[0] for j in cur.execute(f'''SELECT id_in_count FROM Dishes WHERE Dish = "{i}"''').fetchall()])

# nums = [int(i[0]) for i in cur.execute(f'''SELECT Number_of FROM Data WHERE Dish="{dish}"''').fetchall()]
# days = [i[0] for i in cur.execute(f'''SELECT Day FROM Data WHERE Dish="{dish}"''').fetchall()]


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_login = types.KeyboardButton("Войти")
    btn_logup = types.KeyboardButton("Регистрация")
    markup.add(btn_login, btn_logup)
    bot.reply_to(message,
                 """Привет! Я Бот, который поможет тебе со сбором статистики! Для начала работы войдите или зарегистрируйтесь.""".format(
                     message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, logging)


def logging(message):
    global USERS
    if message.text == 'Войти':
        if str(message.chat.id) in USERS:
            bot.reply_to(message, """Успешно!""")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_do_graph = types.KeyboardButton('Посмотреть статистику')
            btn_add_data = types.KeyboardButton('Добавить данные')
            btn_help = types.KeyboardButton('Помощь')
            markup.add(btn_do_graph, btn_add_data, btn_help)
            bot.register_next_step_handler(message, doing(message))
        else:
            bot.reply_to(message, """Сначала нужно зарегистрироваться!""")
            bot.register_next_step_handler(message, logging)
    elif message.text == 'Регистрация':
        if str(message.chat.id) in USERS:
            bot.reply_to(message, """Такой пользователь уже зарегистрирован!""")
            bot.register_next_step_handler(message, logging)
        else:
            bot.reply_to(message, """Регистрация прошла успешно!""")
            cur.execute(f'''INSERT INTO Users id_telegram VALUES ("{message.chat.id}")''')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_do_graph = types.KeyboardButton('Посмотреть статистику')
            btn_add_data = types.KeyboardButton('Добавить данные')
            btn_help = types.KeyboardButton('Помощь')
            markup.add(btn_do_graph, btn_add_data, btn_help)
            bot.register_next_step_handler(message, doing(message))


def doing(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_do_graph = types.KeyboardButton('Посмотреть статистику')
    btn_add_data = types.KeyboardButton('Добавить данные')
    btn_help = types.KeyboardButton('Помощь')
    markup.add(btn_do_graph, btn_add_data, btn_help)
    bot.reply_to(message,
                 """Выберите действие:""".format(
                     message.from_user), reply_markup=markup)
    if message.text == 'Посмотреть статистику':
        pass
    elif message.text == 'Добавить данные':
        pass
    else:
        pass

def see_statistic(message):
    pass

def add_items(message):
    pass


# def send_message(message):
#     global days, dish, nums
#     if message.text == 'Посмотреть статистику':
#         network = NNW(nums)
#         for i in data:
#             graph_builder(days, nums, dish)
#             bot.send_photo(message.chat.id, open('./save.png', 'rb'))
#             if network.relevant_of_prod:
#                 bot.send_message(message.from_user.id,
#                                  f'Советую завтра сделать акцент на {dish.lower()}. (Возможно Вы реализуете {network.medium_of_list()} шт)')
#             else:
#                 bot.send_message(message.from_user.id,
#                                  f'Не советую делать акцент на {dish.lower()}, так как у него низкая релевантность. (Возможно Вы реализуете {network.medium_of_list()} шт)')
#     elif message.text == 'Помощь':
#         bot.send_message(message.from_user.id,
#                          f'Для получения статистики нажмите "Посмотреть статистику", для добавления данных нажмите "Добавить данные".')
#     elif message.text == 'Добавить данные':
#         msg = bot.send_message(message.from_user.id,
#                                f'''Успешно!''')


bot.polling(none_stop=True, interval=0)
