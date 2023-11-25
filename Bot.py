from telebot import *
from telebot import types
from Token import token as t
import sqlite3
from NeuralNetWork import NeuralNetWork as NNW
from graph_buider import graph_builder

start = False
bot = telebot.TeleBot(t)
con = sqlite3.connect('WorkFuelTelegramBot')
cur = con.cursor()
data = cur.execute(f"""SELECT * FROM Statistics""").fetchall()
dish = "Салат"
nums = [int(i[0]) for i in cur.execute(f'''SELECT Number_of FROM Data WHERE Dish="{dish}"''').fetchall()]
days = [i[0] for i in cur.execute(f'''SELECT Day FROM Data WHERE Dish="{dish}"''').fetchall()]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Посмотреть статистику")
    btn2 = types.KeyboardButton("Добавить данные")
    btn3 = types.KeyboardButton('Помощь')
    markup.add(btn1, btn2, btn3)
    bot.reply_to(message, """Привет! Я Бот, который поможет тебе со сбором статистики! Нажмите 'Помощь'.""".format(
        message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_message(message):
    global days, dish, nums
    if message.text == 'Посмотреть статистику':
        network = NNW(nums)
        for i in data:
            graph_builder(days, nums, dish)
            bot.send_photo(message.chat.id, open('./save.png', 'rb'))
            if network.relevant_of_prod:
                bot.send_message(message.from_user.id,
                                 f'Советую завтра сделать акцент на {dish.lower()}. (Возможно Вы реализуете {network.medium_of_list()} шт)')
            else:
                bot.send_message(message.from_user.id,
                                 f'Не советую делать акцент на {dish.lower()}, так как у него низкая релевантность. (Возможно Вы реализуете {network.medium_of_list()} шт)')
    elif message.text == 'Помощь':
        bot.send_message(message.from_user.id,
                         f'Для получения статистики нажмите "Посмотреть статистику", для добавления данных нажмите "Добавить данные".')
    elif message.text == 'Добавить данные':
        msg = bot.send_message(message.from_user.id,
                               f'''Пришлите мне данные, которые надо добавить для создания статистики.\nПример: Куриная котлета-6-Пн''')


bot.polling(none_stop=True, interval=0)
