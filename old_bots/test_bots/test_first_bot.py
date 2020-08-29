import telebot

# Импортируем библиотеку для работы с .env файлом
import os
from dotenv import load_dotenv
from telebot import apihelper

# Указываем путь к .env файлу
env_path = '../.env'
# Считываем токен из .env файла
load_dotenv(dotenv_path=env_path)
token = os.getenv('HANGMAN_TELEGRAM_TOKEN')

# Указываем токен
bot = telebot.TeleBot(token)

# proxy socks5
apihelper.proxy = {'https': 'socks5://72322931:RldoaIVa@grsst.s5.opennetwork.cc:999'}


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message.text)


bot.polling(none_stop=True, interval=0)
