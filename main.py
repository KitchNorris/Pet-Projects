from tradingview_ta import TA_Handler, Interval, Exchange
import time
import telebot
from telebot import types


bols = [] # Список котировок от пользователя (symbol)
srcs = [] # Страны торгов под котировки (screener)
exs = [] # Биржи для котировок (exchange)
borders = [] # Значения для алертов
lastb = []
laste = []
lasts = []


bot = telebot.TeleBot("5691025377:AAFdwBJczrn17PtHt7R0RtRh9uNjlpZaAII")


markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #Добавление клавиатуры
btn1 = types.KeyboardButton('Добавить котировку')
btn2 = types.KeyboardButton('Удалить котировку')
btn3 = types.KeyboardButton('Мой список котировок')
btn4 = types.KeyboardButton('Отслеживать')
markup.add(btn1, btn2, btn3, btn4)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.chat.id, text='Welcome to the club, buddy!', reply_markup=markup)


@bot.message_handler(content_types='text')
def menu(message):
    if message.text == "Добавить котировку":
        markup1=types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn11=types.KeyboardButton("Далее к бирже")
        markup1.add(btn11)
        bot.send_message(message.chat.id, 'Введите символ котировки и нажмите далее к бирже', reply_markup=markup1)
        bot.register_next_step_handler(message, add_bols)
    elif message.text == "Далее к бирже":
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn11 = types.KeyboardButton("Далее к рынку")
        markup1.add(btn11)
        bot.send_message(message.chat.id, 'Введите биржу котировки и нажмите далее к рынку', reply_markup=markup1)
        bot.register_next_step_handler(message, add_exs)
    elif message.text == "Далее к рынку":
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn11 = types.KeyboardButton("Далее")
        markup1.add(btn11)
        bot.send_message(message.chat.id, 'Введите рынок котировки и нажмите далее', reply_markup=markup1)
        bot.register_next_step_handler(message, add_srcs)
    elif message.text == "Далее":
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn11 = types.KeyboardButton("Меню")
        markup1.add(btn11)
        bot.send_message(message.chat.id, 'Введите границу торгов и нажмите меню', reply_markup=markup1)
        bot.register_next_step_handler(message, add_borders)
    elif message.text == "Меню":
        b = lastb.pop()
        last_add = TA_Handler(
            symbol=b,
            screener=lasts.pop(),
            exchange=laste.pop(),
            interval=Interval.INTERVAL_1_MINUTE,
        )  # Последняя добавленная котировка

        last = last_add.get_analysis().indicators['open']
        bot.send_message(message.chat.id, f'Вы добавили: {b} / Текущее значение котировки: {last}', reply_markup=markup)

    elif message.text == "Удалить котировку":
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn11 = types.KeyboardButton("Завершить")
        markup1.add(btn11)
        bot.send_message(message.chat.id, 'Введите символ котировки, чтобы удалить, и нажмите завершить', reply_markup=markup1)
        bot.register_next_step_handler(message, pop_kot)
    elif message.text == "Завершить":
        bot.send_message(message.chat.id, 'Текущий список котировок:', reply_markup=markup)
        if len(bols) == 0:
            bot.send_message(message.chat.id, 'Список пуст')
        else:
            x = 0
            while x < len(bols):
                all_kot = TA_Handler(
                    symbol=bols[x],
                    screener=srcs[x],
                    exchange=exs[x],
                    interval=Interval.INTERVAL_1_MINUTE,
                )
                alles = all_kot.get_analysis().indicators['open']
                bot.send_message(message.chat.id, f'Котировка: {bols[x]} | Цена котировки: {alles}')
                x += 1

    elif message.text == "Мой список котировок":
        if len(bols) == 0:
            bot.send_message(message.chat.id, 'Список пуст')
        else:
            x = 0
            while x < len(bols):
                all_kot = TA_Handler(
                    symbol=bols[x],
                    screener=srcs[x],
                    exchange=exs[x],
                    interval=Interval.INTERVAL_1_MINUTE,
                )
                alles = all_kot.get_analysis().indicators['open']
                bot.send_message(message.chat.id, f'Котировка: {bols[x]} | Цена котировки: {alles}')
                x += 1

    elif message.text == "Отслеживать":
        bot.send_message(message.chat.id, 'Запускаю отслеживание!')
        while True:
            x = 0
            while x < len(bols):
                all_kot = TA_Handler(
                    symbol=bols[x],
                    screener=srcs[x],
                    exchange=exs[x],
                    interval=Interval.INTERVAL_1_MINUTE,
                )
                alles = all_kot.get_analysis().indicators['open']
                if alles >= borders[x]:
                    bot.send_message(message.chat.id, f'Alert!!! {bols[x]} превысила {borders[x]}')
                    bot.send_message(message.chat.id, f'{bols[x]}: {alles}!!!')
                    time.sleep(60)
                x += 1
            time.sleep(15)


def add_bols(message): # Добавление котировок
    bols.append(message.text)
    lastb.append(message.text)
    print(bols)


def add_exs(message): # Добавление рынков котировок
    exs.append(message.text)
    laste.append(message.text)
    print(exs)


def add_srcs(message): # Добавление биржи
    srcs.append(message.text)
    lasts.append(message.text)
    print(srcs)


def add_borders(message): # Добавление пограничных значений для вызова алертов
    borders.append(int(message.text))
    print(borders)


def pop_kot(message): # Удаление элемента из списков
    y = 0
    while y < len(bols):
        if bols[y] == message.text:
            bols.pop(y)
            srcs.pop(y)
            exs.pop(y)
            borders.pop(y)
            bot.send_message(message.chat.id, 'Котировка удалена!')
            break
        elif bols[y] != message.text:
            y += 1


bot.infinity_polling()



