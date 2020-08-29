"""
GamesBot на Heroku.
"""

# Библеотека бота
import telebot

import os

# Библеотека класс переводчика
from gamesBot import Translation

# Библеотека игры "Слоты"
from gamesBot import Slots

# Библеотека игры "Блэкджек"
from gamesBot import Blackjack

# Библеотека игры "Висельница"
from gamesBot import Hangman

# Библеотека игры "Крестики-нолики" для группового чата
from gamesBot import TTT_group

# Библеотека игры "Крестики-нолики" для приватного чата
from gamesBot import XO_class

# Импорт функции для генерации главного меню
from gamesBot import gen_menu_keyboard

# Библеотека игры "Правда или Действие"
from gamesBot import TorA_core

# Библеотека логирования
import logging

# Библеотека поисковика собеседника
from gamesBot import Dating_class

# Библиотека для создания Flask веб-приложений
from flask import Flask, request

# Библиотека для работы с таблицами базы данных
from flask_sqlalchemy import SQLAlchemy

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

# Вывод в консоль сообщения о запуске бота
logging.info('Started')

# Указываем токен и создаем бота
token = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(token, threaded=False)

# Создание Flask-приложения
app = Flask(__name__)

# Настройка конфигурации базы данных для Flask-приложения
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Объект базы данных
db = SQLAlchemy(app)


class Language(db.Model):
    """
    Класс таблицы 'lang' из базы данных.
    """
    __tablename__ = 'lang'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Integer, default=0)


def tables_preparation(message):
    """
    Функция, проверяющая есть ли уже в таблице 'lang' юзер.
    Если нет, то добавляет его и выставляет русский язык.

    :param message: Сообщение
    """
    chat_id = message.from_user.id

    if db.session.query(db.exists().where(Language.id == chat_id)).scalar() is False:
        db.session.add(Language(id=chat_id))
    db.session.commit()


def get_language_from_db(chat_id):
    """
    Функция берет язык из таблицы 'lang' по ID пользователя.

    :param chat_id: ID пользователя.
    :return: Язык.
    """
    chat_lang = db.session.query(Language).filter(Language.id == chat_id).one()
    db.session.commit()

    return chat_lang.lang


# Поток обработки основного меню
@bot.message_handler(commands=['start'])
def welcome(message):
    """
    Обработчик команды /start.

    :param message: Сообщение.
    """
    if Dating_class.check_filling_status(message.from_user.id):
        return
    if XO_class.check_id_in_lobby_dict(message.from_user.id, message.chat.type):
        return

    tables_preparation(message)
    chat_lang = get_language_from_db(message.from_user.id)
    Translation.set_language(message.from_user.id, chat_lang)

    markup = gen_menu_keyboard(message.from_user.id, message.chat.type)
    bot.send_message(message.chat.id, Translation.get_menu_expression("choose_game", user_id=message.from_user.id),
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    """
    Обработчик команды /help.

    :param message: Сообщение.
    """
    if Dating_class.check_filling_status(message.from_user.id):
        pass
    elif XO_class.check_id_in_lobby_dict(message.from_user.id, message.chat.type):
        pass
    else:
        tables_preparation(message)
        chat_lang = get_language_from_db(message.from_user.id)
        Translation.set_language(message.from_user.id, chat_lang)

        bot.send_message(message.chat.id, Translation.get_menu_expression("help", user_id=message.from_user.id))


@bot.message_handler(content_types=['text', 'photo'])
def dating_handler(message):
    """
    Обработчик фотографий для поисковика.

    :param message: Сообщение.
    """
    print(message)
    if Dating_class.check_filling_status(message.from_user.id):
        Dating_class.dating_message_handler(bot, message)


@bot.callback_query_handler(func=lambda call: True)
def main_menu_callback(call):
    """
    Обработчик колбеков главного меню.

    :param call: Колбек.
    """
    chat_lang = get_language_from_db(call.from_user.id)
    Translation.set_language(call.from_user.id, chat_lang)

    if call.data == "Menu":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              reply_markup=gen_menu_keyboard(call.from_user.id, call.message.chat.type),
                              text=Translation.get_menu_expression(key="choose_game", user_id=call.from_user.id),
                              message_id=call.message.message_id)
        Translation.flag = None
    if call.data == "language":
        Translation.switch_language(call.from_user.id)

        chat_lang = db.session.query(Language).filter(Language.id == call.from_user.id).one()
        chat_lang.lang = Translation.get_language(call.from_user.id)
        db.session.commit()

        bot.edit_message_text(chat_id=call.message.chat.id,
                              reply_markup=gen_menu_keyboard(call.from_user.id, call.message.chat.type),
                              text=Translation.get_menu_expression(key="choose_game", user_id=call.from_user.id),
                              message_id=call.message.message_id)
    elif call.data in Blackjack.call_list:
        Blackjack.get_callback(call, bot)
    elif call.data in Hangman.call_list:
        Hangman.get_callback(call, bot, Translation.get_player_language(call.from_user.id))
    elif call.data in TTT_group.call_list:
        TTT_group.get_callback(call, bot)
    elif call.data == "Slots" or call.data == 'spin':
        Slots.callback_inline(call, bot)
    elif call.data in XO_class.call_list and call.message.chat.type == "private":
        XO_class.xo_lobby_handler(call=call, bot=bot,
                                  menu_keyboard=gen_menu_keyboard(call.from_user.id, call.message.chat.type))
        XO_class.xo_game_core(call, bot, gen_menu_keyboard(call.from_user.id, call.message.chat.type))
    elif call.data in Dating_class.call_list and call.message.chat.type == "private":
        Dating_class.dating_lobby_handler(call, bot, gen_menu_keyboard(call.from_user.id, call.message.chat.type))
    elif call.data in TorA_core.call_list:
        TorA_core.main_handler(bot, call)


@app.route('/' + token, methods=['POST'])
def getMessage():
    """
    Получение сообщений.
    """
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    """
    Установка вебхука.
    """
    bot.remove_webhook()
    bot.set_webhook(url='https://games-bot-for-telegram.herokuapp.com/' + token)
    return "!", 200


if __name__ == "__main__":
    # Запуск бота
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
