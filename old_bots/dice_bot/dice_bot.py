# Подключаем модуль для Телеграма
import telebot

# Подключаем модуль для регистрации событий
import logging

# Импортируем типы из модуля, чтобы создавать кнопки
import types

# Импортируем библиотеку для работы с .env файлом
import os
from dotenv import load_dotenv

# Подключаем модуль случайных чисел
import random

# Настройка формата вывода сообщений
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Вывод в консоль сообщения о запуске бота
logging.info('Started')

# Указываем путь к .env файлу
env_path = '../.env'
# Считываем токен из .env файла
load_dotenv(dotenv_path=env_path)
token = os.getenv('DICE_TELEGRAM_TOKEN')

# Указываем токен
bot = telebot.TeleBot(token)

# Грани игральной кости
dice = [1, 2, 3, 4, 5, 6]


# Обработчик сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Играть" or message.text == "играть":
        # Готовим клавиатуру
        keyboard = types.ReplyKeyboardMarkup()
        # И добавляем в неё кнопки
        first_button = types.KeyboardButton("Бросить кости")
        second_button = types.KeyboardButton("Выйти")
        keyboard.add(first_button, second_button)
        bot.send_message(message.chat.id, 'Бросьте кости', reply_markup=keyboard)
    elif message.text == "Бросить кости":
        chance(message)
    elif message.text == "Выйти":
        # Убираем клавиатуру
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Выход', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.chat.id, "Напишите \"Играть\"")
    else:
        print(message.text)


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def chance(message):
    # Бросаем кости
    user_first_dice = random.choice(dice)
    user_second_dice = random.choice(dice)
    bot_first_dice = random.choice(dice)
    bot_second_dice = random.choice(dice)

    # Выводим результаты бросков
    throw = "Вы кинули:  \t" + str(user_first_dice) + '️⃣' + str(user_second_dice) + '️⃣' + '\n' \
            + "Бот кинул: \t" + str(bot_first_dice) + '️⃣' + str(bot_second_dice) + '️⃣' + '\n\n'

    user_sum = user_first_dice + user_second_dice
    bot_sum = bot_first_dice + bot_second_dice

    if bot_sum > user_sum:
        bot.send_message(message.chat.id, throw + "Ты проиграл")
    elif bot_sum == user_sum:
        bot.send_message(message.chat.id, throw + "Ничья")
    else:
        bot.send_message(message.chat.id, throw + "Ты выиграл!!!")


# Запускаем постоянный опрос бота в Телеграме
bot.polling(none_stop=True, interval=0)

# Вывод в консоль сообщения об окончании работы бота
logging.info('Finished')