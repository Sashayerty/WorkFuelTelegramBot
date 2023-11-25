from telebot import *
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
nums = cur.execute(f'''SELECT Number_of FROM Data WHERE Dish="{dish}"''').fetchall()
days = [i[0] for i in cur.execute(f'''SELECT Day FROM Data WHERE Dish="{dish}"''').fetchall()]


@bot.message_handler()
def send_welcome(message):
    global start, nums, days, dish
    if not start and message.text != '/statistics' and message.text != '/help':
        bot.reply_to(message, """Привет! Я Бот, который поможет тебе со сбором статистики! Напиши /help.""")
        start = True
    elif message.text == '/statistics':
        start = True
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
    elif message.text == '/help':
        start = True
        bot.send_message(message.from_user.id, f'Для получения статистики напиши мне /statistics, для добавления данных напиши /add_data.')
    elif message.text == '/add_data':
        start = True
        bot.send_message(message.from_user.id, f'''Пришлите мне данные, которые надо добавить для создания статистики.\n
                                                Пример: Куриная котлета-6шт-Пн''')
    else:
        start = True
        bot.send_message(message.from_user.id, f'Для помощи напиши /help.')


bot.polling(none_stop=True, interval=0)
