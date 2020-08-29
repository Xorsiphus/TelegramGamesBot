# - *- coding: utf- 8 - *-
import telebot
from dotenv import load_dotenv
import os
import random
from telebot import types

env_path = '.env'
config_path = 'config.ini'
load_dotenv(dotenv_path=env_path)
bot = telebot.TeleBot(os.getenv('SLOTSBOT_TELEGRAM_TOKEN'))


# Поток обработки основного меню
@bot.message_handler(commands=['start'])
def welcome(message):
    # Приветствующий стикер
    sti = open('top_heil.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # Подготовка меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    f = open(config_path, 'r')
    lang = f.read(2)
    f.close()
    print(lang)
    if lang == 'EN':
        m1 = types.KeyboardButton("Random number")
        m2 = types.KeyboardButton("Play \"Slots\"")
        m3 = types.KeyboardButton("Change language")
    else:
        m1 = types.KeyboardButton("Случайное число")
        m2 = types.KeyboardButton("Играть в \"Слоты\"")
        m3 = types.KeyboardButton("Сменить язык")
    markup.add(m1, m2, m3)

    # Отправка сообщения с приветствием и меню
    if lang == 'EN':
        bot.send_message(message.chat.id,
                         "Welcome, {0.first_name}! \n<b>I'm - {1.first_name}</b>".format(message.from_user,
                                                                                       bot.get_me()),
                         parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         "Добро пожаловать, {0.first_name}! \n<b>Я - {1.first_name}</b>".format(message.from_user,
                                                                                                bot.get_me()),
                         parse_mode='html', reply_markup=markup)


# Поток обработки сообщений
@bot.message_handler(content_types=['text'])
def respeak(message):
    print(message.text)

    # Кнопка случайного числа
    if message.text == 'Random number' or message.text == 'Случайное число':
        bot.send_message(message.chat.id, str(random.randint(0, 1000)))

    # Сообщение + Кнопка для игры в "Слоты"
    elif message.text == "Play \"Slots\"" or message.text == "Играть в \"Слоты\"":
        markup = types.InlineKeyboardMarkup(row_width=3)
        f = open(config_path, 'r')
        lang = f.read(2)
        f.close()
        if lang == 'EN':
            b = types.InlineKeyboardButton("Spin!", callback_data='spin')
        else:
            b = types.InlineKeyboardButton("Крутить!", callback_data='spin')
        markup.add(b)
        if lang == 'EN':
            bot.send_message(message.chat.id, "Slots", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Слоты", reply_markup=markup)

    elif message.text == 'Change language' or message.text == 'Сменить язык':
        f = open(config_path, 'r')
        lang = f.read(2)
        f.close()
        if lang == 'EN':
            f = open(config_path, 'w')
            f.write("RU")
            f.close()
            bot.send_message(message.chat.id, "Язык успешно изменён!")
            welcome(message)
        else:
            f = open(config_path, 'w')
            f.write("EN")
            f.close()
            bot.send_message(message.chat.id, "Language successfully changed!")
            welcome(message)

    # Обработка остальных сообщений
    # else:
    #    bot.send_message(message.chat.id, "Не знаю что ответить")


# Поток обработки callback'ов (для inline кнопок)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:

        # Код при нажатии на "Play Slots" в меню (сама игра "Слот-Машина")
        if call.data == 'spin':
            i = 0
            array = []

            # Генерация случайного списка, от которого зависит выигрыш
            while i < 9:
                array.append(random.randint(0, 4))
                i = i + 1
            new_array = []
            i = 0

            # Замена случайных чисел на картинки для наглядности
            while i < 9:
                if array[i] == 0:
                    new_array.append("7️⃣")
                elif array[i] == 1:
                    new_array.append("🍒")
                elif array[i] == 2:
                    new_array.append("🍋")
                elif array[i] == 3:
                    new_array.append("🍎")
                elif array[i] == 4:
                    new_array.append("🍉")
                i += 1

            # Удаление inline-кнопки у предыдущего сообщения (остаётся только сообщение "Slots: ")
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=None, text=call.message.text,
                                  message_id=call.message.message_id)

            # Подготовка inline-кнопок "Spin!" и "Exit" к следующему сообщению
            markup = types.InlineKeyboardMarkup(row_width=3)
            f = open('config.ini', 'r')
            lang = f.read(2)
            f.close()
            if lang == 'EN':
                b1 = types.InlineKeyboardButton("Spin!", callback_data='spin')
                b2 = types.InlineKeyboardButton("Exit", callback_data='exit')
            else:
                b1 = types.InlineKeyboardButton("Крутить!", callback_data='spin')
                b2 = types.InlineKeyboardButton("Выход", callback_data='exit')
            markup.add(b1, b2)

            # Крепление inline-меню (кнопки "Spin!" и "Exit") и вывод слотов пользователю
            if lang == 'EN':
                bot.send_message(call.message.chat.id, "Your slots:\n{}{}{}\n{}{}{}\n{}{}{}".format(*new_array),
                                 reply_markup=markup)
            else:
                bot.send_message(call.message.chat.id, "Ваши слоты:\n{}{}{}\n{}{}{}\n{}{}{}".format(*new_array),
                                 reply_markup=markup)

            # Проверка выигрыша (на данный момент просто проверка всех строк и столбцов)
            # При удовлетворении условию выводится уведомление с поздравлением
            if new_array[0] == new_array[1] == new_array[2] or new_array[3] == new_array[4] == new_array[5] or \
                    new_array[6] == new_array[7] == new_array[8] or new_array[0] == new_array[3] == new_array[6] or \
                    new_array[1] == new_array[4] == new_array[7] or new_array[2] == new_array[5] == new_array[8]:
                bot.answer_callback_query(callback_query_id=call.id, text="Jackpot!!!", show_alert=True)

        # Код при нажатии на "Exit" в игре "Slots" (пока что просто удаление inline-кнопок "Spin!" и "Exit")
        elif call.data == 'exit':
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=None, text=call.message.text,
                                  message_id=call.message.message_id)


bot.polling(none_stop=True)
