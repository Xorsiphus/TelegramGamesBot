# - *- coding: utf- 8 - *-
# Библеотека бота
import telebot

# Библеотека для извлечения токена из файла
from dotenv import load_dotenv
import os

# Библеотека класс переводчика
from gamesBot import Translation

# Библеотека игры "Слоты"
from gamesBot import Slots

# Библеотека игры "Блэкджек"
from gamesBot import Blackjack

# Библеотека игры "Висельница"
from gamesBot import Hangman

from gamesBot import TTT_group

from gamesBot import XO_class
from gamesBot import gen_menu_keyboard

from gamesBot import TorA_core

# Библеотека логирования
import logging

# Библеотека поисковика собеседника
from gamesBot import Dating_class

env_path = '../.env'
load_dotenv(dotenv_path=env_path)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

logging.info('Started')

# secret = ''
# url = 'https://.pythonanywhere.com/' + secret
# bot = telebot.TeleBot(os.getenv('SLOTSBOT_TELEGRAM_TOKEN'), threaded=False)
# bot.remove_webhook()
# bot.set_webhook(url=url)
# app = Flask(__name__)


# @app.route('/' + secret, methods=['POST'])
# def webhook():
#     update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
#     bot.process_new_updates([update])
#     return 'ok', 200

bot = telebot.TeleBot(os.getenv('SLOTSBOT_TELEGRAM_TOKEN'))
bot.remove_webhook()


# Поток обработки основного меню
@bot.message_handler(commands=['start'])
def welcome(message):
    if Dating_class.check_filling_status(message.from_user.id):
        return
    if XO_class.check_id_in_lobby_dict(message.from_user.id, message.chat.type):
        return
    Translation.set_lang(message.from_user)
    markup = gen_menu_keyboard(message.from_user.id, message.chat.type)
    bot.send_message(message.chat.id, Translation.get_menu_expression("choose_game", user_id=message.from_user.id),
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    if Dating_class.check_filling_status(message.from_user.id):
        pass
    elif XO_class.check_id_in_lobby_dict(message.from_user.id, message.chat.type):
        pass
    else:
        bot.send_message(message.chat.id, Translation.get_menu_expression("help", user_id=message.from_user.id))


@bot.message_handler(commands=['playHangman'])
def handle_text(message):
    if Dating_class.check_filling_status(message.from_user.id):
        return
    if XO_class.check_id_in_lobby_dict(message.from_user.id, message.chat.type):
        return
    message.text = Translation.get_menu_expression(key="Hangman", user_id=message.from_user.id)


@bot.message_handler(content_types=['text', 'photo'])
def dating_handler(message):
    print(message)
    if Dating_class.check_filling_status(message.from_user.id):
        Dating_class.dating_message_handler(bot, message)


@bot.callback_query_handler(func=lambda call: True)
def main_menu_callback(call):
    if call.data == "Menu":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              reply_markup=gen_menu_keyboard(call.from_user.id, call.message.chat.type),
                              text=Translation.get_menu_expression(key="choose_game", user_id=call.from_user.id),
                              message_id=call.message.message_id)
    if call.data == "language":
        Translation.switch_language(call.from_user.id)
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
    elif call.data == "Dice":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              reply_markup=gen_menu_keyboard(call.from_user.id, call.message.chat.type + "Dice"),
                              text=Translation.get_menu_expression(key="choose_game", user_id=call.from_user.id),
                              message_id=call.message.message_id)
    elif call.data in TorA_core.call_list:
        TorA_core.main_handler(bot, call)


if __name__ == "__main__":
    bot.polling(none_stop=True)
    logging.info('Finished')
