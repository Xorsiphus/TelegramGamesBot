# Телеграм бот для игры в блэкджек

# Подключаем модуль для Телеграма
import telebot

# Подключаем модуль для регистрации событий
import logging

# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types

# Импортируем библиотеку для работы с .env файлом
import os
from dotenv import load_dotenv

# Импортируем библиотеку для работы со временем
import time

from blackjack import Blackjack
from player import Player
from translation import Translation

import fileinput

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

ID = 0

# Указываем путь к .env файлу
env_path = 'gamebotsfortelegram/.env'
# Считываем токен из .env файла
load_dotenv(dotenv_path=env_path)
token = os.getenv('BLACKJACK_TELEGRAM_TOKEN')
secret = os.getenv('SECRET_BLACKJACK')
URL = "https://neverr1n.pythonanywhere.com/" + str(secret)

# Указываем токен
bot = telebot.TeleBot(token, threaded=False)

# Настраиваем webhook
bot.remove_webhook()
bot.set_webhook(url=URL)

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    hostname=os.getenv('DB_HOSTNAME'),
    databasename=os.getenv('DB_NAME'),
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class BJ_Stats(db.Model):
    __tablename__ = 'bj_stats'

    id = db.Column(db.Integer, primary_key=True)
    games_amount = db.Column(db.Integer, default=0)
    wins_amount = db.Column(db.Integer, default=0)

class Language(db.Model):
    __tablename__ = 'lang'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Integer, default=0)


# id = '3'
# games_amount = '2'
# wins_amount = '3'

# insert_this = BJ_Stats(id=id, games_amount=games_amount, wins_amount=wins_amount)

# db.session.add(insert_this)
# stat = db.session.query(BJ_Stats).get(1)
# print(str(stat.wins_amount) + "сообщение")
# db.session.commit()

bot_lang = Translation("rus")

players = []


@app.route('/' + secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, bot_lang.get_casino_expression("Hello"))
    time.sleep(1)
    bot.send_message(message.chat.id, bot_lang.get_casino_expression("Help"))


commands = bot_lang.get_casino_expression("Commands")


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, commands)


def gen_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    first_btn = types.KeyboardButton(bot_lang.get_casino_expression("Blackjack"))
    second_btn = types.KeyboardButton(bot_lang.get_casino_expression("Profile"))
    third_btn = types.KeyboardButton(bot_lang.get_casino_expression("Language"))
    forth_btn = types.KeyboardButton(bot_lang.get_casino_expression("Exit"))
    keyboard.add(first_btn, second_btn, third_btn, forth_btn)

    return keyboard


def gen_play_blackjack_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    first_btn = types.KeyboardButton(bot_lang.get_casino_expression("Play"))
    second_btn = types.KeyboardButton(bot_lang.get_casino_expression("Menu"))
    keyboard.add(first_btn, second_btn)

    return keyboard


def gen_game_blackjack_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    first_btn = types.KeyboardButton(bot_lang.get_casino_expression("TakeCard"))
    second_btn = types.KeyboardButton(bot_lang.get_casino_expression("DoNotTakeCard"))
    third_btn = types.KeyboardButton(bot_lang.get_casino_expression("LeaveGame"))
    keyboard.add(first_btn, second_btn, third_btn)

    return keyboard


def gen_change_language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    first_btn = types.KeyboardButton("Русский 🇷🇺")
    second_btn = types.KeyboardButton("English 🇬🇧")
    third_btn = types.KeyboardButton(bot_lang.get_casino_expression("Menu"))
    keyboard.add(first_btn, second_btn, third_btn)

    return keyboard


# Играет ли юзер?  player = Player(message.chat.first_name, message.chat.id, 50)
def checker(player_id):
    for game in players:
        if player_id == game.player.telegram_id:
            return True
    return False


# Найти игрока по ID
def id_found(message):
    while True:
        for game in players:
            if game.player.telegram_id == message.chat.id:
                return game
        player = Player(message.chat.first_name, message.chat.id, 50)
        game = Blackjack(player)
        game.deck.double_deck()
        game.deck.shuffle_deck()
        game.next_round()
        game.lose_the_game()
        players.append(game)


@bot.message_handler(commands=['menu'])
def handle_menu(message):
    keyboard = gen_menu_keyboard()
    bot.send_message(message.chat.id, bot_lang.get_casino_expression("Choose"), reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == bot_lang.get_casino_expression("Blackjack"),
                     content_types=['text'])
def handle_blackjack(message):
    keyboard = gen_play_blackjack_keyboard()
    bot.send_message(message.chat.id, bot_lang.get_casino_expression("Choose"), reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == bot_lang.get_casino_expression("Language"),
                     content_types=['text'])
def handle_change_language(message):
    keyboard = gen_change_language_keyboard()
    bot.send_message(message.chat.id, bot_lang.get_casino_expression("Choose"), reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Русский 🇷🇺",
                     content_types=['text'])
def handle_change_language_to_russian(message):
    chat_id = message.chat.id

    chat_lang = db.session.query(Language).filter(Language.id == chat_id).one()
    chat_lang.lang = 0
    db.session.commit()

    bot_lang.get_player_language = "rus"

    keyboard = gen_menu_keyboard()
    bot.send_message(message.chat.id, bot_lang.get_casino_expression("ChangeLang"), reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "English 🇬🇧",
                     content_types=['text'])
def handle_change_language_to_english(message):
    chat_id = message.chat.id

    chat_lang = db.session.query(Language).filter(Language.id == chat_id).one()
    chat_lang.lang = 1
    db.session.commit()

    bot_lang.get_player_language = "eng"

    keyboard = gen_menu_keyboard()
    bot.send_message(message.chat.id, bot_lang.get_casino_expression("ChangeLang"), reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == bot_lang.get_casino_expression("Profile"),
                     content_types=['text'])
def handle_profile(message):
    user_id = message.from_user.id
    user_stat = db.session.query(BJ_Stats).get(user_id)
    stat = f"{message.from_user.first_name}: {user_stat.games_amount} games, {user_stat.wins_amount} wins"
    bot.send_message(message.chat.id, stat)


def query_to_db_after_game(game, user_id):
    user_stat = db.session.query(BJ_Stats).filter(BJ_Stats.id == user_id).one()
    user_stat.games_amount = user_stat.games_amount + 1
    if game.winner == "Player":
        user_stat.wins_amount = user_stat.wins_amount + 1
    db.session.commit()


@bot.message_handler(func=lambda message: message.text == bot_lang.get_casino_expression("Play"),
                     content_types=['text'])
def handle_play_blackjack(message):
    global players
    if checker(message.chat.id):
        players.remove(id_found(message))

    user_id = message.from_user.id
    if db.session.query(db.exists().where(BJ_Stats.id == user_id)).scalar() is False:
        db.session.add(BJ_Stats(id=user_id))
    db.session.commit()

    player = Player(message.chat.first_name, message.chat.id, 50)
    game = Blackjack(player)
    game.deck.double_deck()
    game.deck.shuffle_deck()
    game.next_round()
    players.append(game)

    if game.stop_the_game:
        bot.send_message(message.chat.id, game.display_result(bot_lang.get_player_language))

        query_to_db_after_game(game, user_id)

        keyboard = gen_play_blackjack_keyboard()
        bot.send_message(message.chat.id, bot_lang.get_casino_expression("ExitFromGame"), reply_markup=keyboard)
        players.remove(game)
    else:
        msg = game.display_first_round(bot_lang.get_player_language)

        keyboard = gen_game_blackjack_keyboard()
        bot.send_message(message.chat.id, msg, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == bot_lang.get_casino_expression("TakeCard"),
                     content_types=['text'])
def handle_take_card(message):
    if checker(message.chat.id):
        id_found(message).next_round()

        player_round_message = id_found(message).display_player_round(bot_lang.get_player_language)
        bot.send_message(message.chat.id, player_round_message)

        if id_found(message).stop_the_game:
            bot.send_message(message.chat.id, id_found(message).display_result(bot_lang.get_player_language))
            query_to_db_after_game(id_found(message), message.from_user.id)
            keyboard = gen_play_blackjack_keyboard()
            bot.send_message(message.chat.id, bot_lang.get_casino_expression("ExitFromGame"), reply_markup=keyboard)
            players.remove(id_found(message))
    else:
        handle_exit(message)


@bot.message_handler(func=lambda message: message.text == bot_lang.get_casino_expression("DoNotTakeCard"),
                     content_types=['text'])
def handle_do_not_take_anymore(message):
    if checker(message.chat.id):
        id_found(message).is_player_active = False

        if checker(message.chat.id):
            while id_found(message).stop_the_game is not True:
                id_found(message).next_round()

            bot.send_message(message.chat.id, id_found(message).display_result(bot_lang.get_player_language))
            query_to_db_after_game(id_found(message), message.from_user.id)
            keyboard = gen_play_blackjack_keyboard()
            bot.send_message(message.chat.id, bot_lang.get_casino_expression("ExitFromGame"), reply_markup=keyboard)
            players.remove(id_found(message))
    else:
        handle_exit(message)


@bot.message_handler(func=lambda message: message.text == bot_lang.get_casino_expression("LeaveGame"),
                     content_types=['text'])
def handle_leave_game(message):
    if checker(message.chat.id):
        players.remove(id_found(message))
        keyboard = gen_play_blackjack_keyboard()
        bot.send_message(message.chat.id, bot_lang.get_casino_expression("LeftGame"), reply_markup=keyboard)
    else:
        handle_exit(message)


@bot.message_handler(func=lambda message: message.text == bot_lang.get_casino_expression("Menu"),
                     content_types=['text'])
def handle_menu(message):
    keyboard = gen_menu_keyboard()
    bot.send_message(message.chat.id, bot_lang.get_casino_expression("ReturnToMenu"), reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == bot_lang.get_casino_expression("Exit"),
                     content_types=['text'])
def handle_exit(message):
    # Убираем клавиатуру
    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, bot_lang.get_casino_expression("GameIsOver"), reply_markup=keyboard)


def set_language(messages):
    char_id = messages[-1].chat.id
    if db.session.query(db.exists().where(Language.id == char_id)).scalar() is False:
        db.session.add(Language(id=char_id))
    db.session.commit()

    chat_lang = db.session.query(Language).filter(Language.id == char_id).one()
    db.session.commit()
    if chat_lang.lang == 0:
        bot_lang.get_player_language = "rus"
    elif chat_lang.lang == 1:
        bot_lang.get_player_language = "eng"


# Функция для смены языка
bot.set_update_listener(set_language)
