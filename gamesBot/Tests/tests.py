"""
Функциональное тестирование ботов.
"""

# Библеотека для извлечения токена из файла
import os
from time import sleep

# Смена текущей директории на /gamesBot для корректной работы
if os.path.basename(os.getcwd()) != 'gamesBot':
    os.chdir(os.path.split(os.getcwd())[:-1][0])

from telebot import types
import telebot

from gamesBot import Translation
from gamesBot import TTT_group
from gamesBot import XO_class
from gamesBot import Dating_class
from gamesBot import gen_menu_keyboard
from gamesBot import Hangman
from gamesBot import Slots
from gamesBot import Blackjack, Card, Deck, Player
from gamesBot import TorA_core

CHAT_ID = -1001349075694
CHAT_ID_2 = -1001411028459
bot = telebot.TeleBot('1199433753:AAFKTK-Y29Fde2haiTj0h57X8HWdjlm0FCs')


def fix_tooManyRequests_err(func):
    """
    Декоратор для обхода ошибки 429 в Телеграме.

    :param func: Функция для декорирования.
    :return: Возращает функцию-обертку.
    """
    def wrapper(self):
        try:
            func(self)
        except Exception as err:
            if str(err)[139:142] == "429":
                time = str(err)[221:]
                for i in range(0, len(time)):
                    if time[i] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        time = time[:i]
                        break
                print("\nНаелся и спит " + time + " сек.")
                sleep(int(time) + 1)
                func(self)
                return
            raise err

    return wrapper


class TestTranslation:
    """
    Класс тестирования Переводчика.
    """
    def test_set_language(self):
        Translation.set_language(723229931, 0)
        assert Translation.get_language(723229931) == 0

        Translation.set_lang(723229931)
        assert Translation.get_language(723229931) == 1

        Translation.set_language(723229931, 0)
        assert Translation.get_language(723229931) == 0

        Translation.set_language(723229931, 1)
        assert Translation.get_language(723229931) == 1

    def test_get_expressions(self):
        Translation.set_language(723229931, 0)

        assert Translation.get_menu_expression("TorA", 723229931) == "Правда или Действие!"
        assert Translation.get_bj_expression("TakeCard", 723229931) == "Взять ещё карту"
        assert Translation.get_hangman_exp("end_message", 723229931) == "Игра окончена"
        assert Translation.get_slots_menu_expression("slots", 723229931) == "Слоты"
        assert Translation.get_xo_log_expression("log - del error") == "Лобби {0} не удалено!"
        assert Translation.get_xo_menu_expression("disconnect msg for P2", 723229931) == "Вы покинули лобби!"
        assert Translation.get_dating_log_expression("msg edit error") == "edit message error: {0}"
        assert Translation.get_dating_menu_expression("profile_error", 723229931) == "Сначала необходимо заполнить " \
                                                                                     "профиль!"
        assert Translation.get_tora_menu_expression("exit", 723229931) == "Главное меню"

    def test_switch_language(self):
        Translation.set_language(723229931, 0)
        Translation.switch_language(723229931)

        assert Translation.get_menu_expression("TorA", 723229931) == "True or Action!"
        assert Translation.get_bj_expression("TakeCard", 723229931) == "Take card"
        assert Translation.get_hangman_exp("end_message", 723229931) == "Game over"
        assert Translation.get_slots_menu_expression("slots", 723229931) == "Slots"
        assert Translation.get_xo_menu_expression("disconnect msg for P2", 723229931) == "You left the lobby!"
        assert Translation.get_dating_menu_expression("profile_error",
                                                      723229931) == "First you need to fill out a profile!"
        assert Translation.get_tora_menu_expression("exit", 723229931) == "Main menu"

        Translation.switch_language(723229931)

        assert Translation.get_menu_expression("TorA", 723229931) == "Правда или Действие!"


class TestDatingOption:
    """
    Класс тестирования Поисковика.
    """
    def test_init_default_player_info(self):
        assert {"name": "Иван", "city": "Расия", "age": 9, "image": "dating_option/images/default.jpg",
                "fill_out_flag": False, "username": "undefined"} == Dating_class.init_default_player_info()

    def test_check_id_in_lobby_dict_not_in(self):
        assert Dating_class.check_filling_status(3) == 0

    def test_init_player(self):
        Dating_class.init_player(3)
        Dating_class.set_profile_flag(3)
        assert Dating_class.check_filling_status(3) == 1

    def test_gen_skip_markup(self):
        markup = Dating_class.gen_skip_markup(3)
        assert markup

    def test_get_unique_player_id_not_in(self):
        assert Dating_class.get_unique_player_id(3)

    def test_check_id_in_lobby_dict_in(self):
        assert Dating_class.check_filling_status(3) == 1

    def test_check_id_profile_private(self):
        assert Dating_class.check_id_profile(3, 'private')

    def test_check_id_profile_supergroup(self):
        assert Dating_class.check_id_profile(3, 'supergroup') == 0

    def test_gen_dating_markup(self):
        markup = Dating_class.gen_dating_markup(3)
        assert markup

    def test_gen_finder_markup(self):
        markup = Dating_class.gen_finder_markup(3)
        assert markup

    def test_next_filler_step(self):
        temp = Dating_class.check_filling_status(3)
        Dating_class.next_filler_step(3)
        assert Dating_class.check_filling_status(3) == temp + 1

    def test_gen_player_profile(self):
        assert Dating_class.gen_player_profile(3)

    def test_set_profile_flag(self):
        Dating_class.init_player(11)
        temp = Dating_class.check_id_profile(11, 'private')
        Dating_class.set_profile_flag(11)
        assert Dating_class.check_id_profile(11, 'private') != temp

    def test_get_needed_phrase(self):
        Dating_class.init_player(12)
        assert Dating_class.get_needed_phrase(12) == "Введите имя:"

    @fix_tooManyRequests_err
    def test_dating_lobby_handler_start(self):
        local_message_id = bot.send_message(CHAT_ID, 'text').message_id
        local_params = {'text': r'https://web.telegram.org/'}
        local_chat = types.Chat(CHAT_ID, "private")
        local_user = types.User(CHAT_ID, False, 'test', 'tset', '👍🏾', 'ru')
        local_message = types.Message(local_message_id, local_user, None, local_chat, "text", local_params, None)
        local_call = types.CallbackQuery(1, local_user, "Dating_start", None, local_message)
        Dating_class.dating_lobby_handler(local_call, bot, gen_menu_keyboard(local_call, local_call.message.chat.type))
        assert Dating_class.check_id_in_lobby_dict(CHAT_ID, 'private')

    @fix_tooManyRequests_err
    def test_dating_lobby_handler_show_profile(self):
        local_message_id = bot.send_message(CHAT_ID, 'text').message_id
        local_params = {'text': r'https://web.telegram.org/'}
        local_chat = types.Chat(CHAT_ID, "private")
        local_user = types.User(15, False, 'test', 'tset', '👍🏾', 'ru')
        local_message = types.Message(local_message_id, local_user, None, local_chat, "text", local_params, None)
        local_call = types.CallbackQuery(1, local_user, "Dating_show_profile", None, local_message)
        Dating_class.dating_lobby_handler(local_call, bot, gen_menu_keyboard(local_call, local_call.message.chat.type))
        assert Dating_class.check_id_in_lobby_dict(CHAT_ID, 'private')

    @fix_tooManyRequests_err
    def test_dating_lobby_handler_fill(self):
        local_message_id = bot.send_message(CHAT_ID, 'text').message_id
        local_params = {'text': r'https://web.telegram.org/'}
        local_chat = types.Chat(CHAT_ID, "private")
        local_user = types.User(15, False, 'test', 'tset', '👍🏾', 'ru')
        local_message = types.Message(local_message_id, local_user, None, local_chat, "text", local_params, None)
        local_call = types.CallbackQuery(1, local_user, "Dating_fill", None, local_message)
        Dating_class.init_player(15)
        Dating_class.dating_lobby_handler(local_call, bot, gen_menu_keyboard(local_call, local_call.message.chat.type))
        profile = Dating_class.gen_player_profile(15)
        assert profile['description'][5:9] == 'Иван'

    @fix_tooManyRequests_err
    def test_show_player_profile(self):
        Dating_class.init_player(CHAT_ID)
        Dating_class.set_profile_flag(CHAT_ID)
        Dating_class.show_player_profile(bot, CHAT_ID, 'private', False)
        assert Dating_class.check_id_in_lobby_dict(CHAT_ID, 'private')

    @fix_tooManyRequests_err
    def test_questionnaire_filler(self):
        local_message_id = bot.send_message(CHAT_ID, 'text').message_id
        local_params = {'text': r'https://web.telegram.org/'}
        local_chat = types.Chat(CHAT_ID, "private")
        local_user = types.User(CHAT_ID, False, 'test', 'tset', '👍🏾', 'ru')
        local_message = types.Message(local_message_id, local_user, None, local_chat, "photo", local_params, None)
        Dating_class.init_player(CHAT_ID)
        Dating_class.set_last_bot_message(CHAT_ID, local_message_id)
        Dating_class.questionnaire_filler(bot, local_message, "Best_Name")
        Dating_class.questionnaire_filler(bot, local_message, "228")
        Dating_class.questionnaire_filler(bot, local_message, "Best_City")
        Dating_class.questionnaire_filler(bot, local_message, "dating_option/images/default.jpg")
        Dating_class.show_player_profile(bot, CHAT_ID, 'private', False)
        assert Dating_class.check_id_profile(CHAT_ID, 'private')


class TestHangman:
    """
    Класс тестирования Виселицы.
    """
    JSON = {'reply_markup': {'inline_keyboard': [
        [{'1': '1'}], [{'1': '1'}], [{'1': '1'}],
        [{'1': '1'}], [{'1': '1'}], [{'1': '1'}],
        [{'1': '', 'callback_data': 'none'}]]}}

    @fix_tooManyRequests_err
    def test_player_founder(self):
        json_chat = '{"message_id": 1, "from": {"id": 723229931, "is_bot": false, "first_name": "О", ' \
                    '"last_name": "К 👌", "language_code": "ru"}, "chat": {"id": 723229931, "first_name": "О", ' \
                    '"last_name": "К 👌", "type": "private"}, "date": 1589208635, "text": "Test"}'
        message = types.Message.de_json(json_chat)
        player = Hangman.player_founder(message)
        assert player

    @fix_tooManyRequests_err
    def test_guess_changer(self):
        player = [123, 0, ['X', 'X', 'X'], ['_', '_', '_'], [], ""]
        Hangman.guess_changer('X', player)
        assert not player[3] == ['_', '_', '_']

    @fix_tooManyRequests_err
    def test_keyboard_func(self):
        player = [123, 0, [], [], ['А', 'Б', 'В'], ""]
        keyboard = Hangman.letters_buttons(player)
        assert keyboard
        keyboard = Hangman.create_keyboard(0)
        keyboard_clone = Hangman.create_keyboard(0)
        assert keyboard
        Hangman.menu_btn_add(keyboard, 0)
        assert not keyboard == keyboard_clone
        keyboard = Hangman.end_keyboard(1)
        assert keyboard

    @fix_tooManyRequests_err
    def test_hp_visual(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        player = [1, 1, ['Т', 'Е', 'С', 'Т'], ['_', '_', '_', '_'], ['А', 'Б', 'В'], 'ТЕСТ']
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "supergroup")
        message = types.Message(message_id, None, None, chat, "text", params, "")
        call = types.CallbackQuery(1, None, "test", None, message)

        Hangman.hp_visual(call, bot, player, '', 0)
        assert player[1] == 1

    @fix_tooManyRequests_err
    def test_new_player(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        player = [0, 0, [], [], [], ""]
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(723229931, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, self.JSON)
        call = types.CallbackQuery(1, user, "ANIMALS", None, message)

        Hangman.new_player(call, bot, player, 0)
        assert player[1] == 6

    @fix_tooManyRequests_err
    def test_hangman(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(723229931, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, self.JSON)

        call = types.CallbackQuery(1, user, "Hangman", None, message)
        Hangman.get_callback(call, bot, 0)
        assert call.data == "Hangman"

        call.data = "ANIMALS"
        Hangman.get_callback(call, bot, 0)
        assert call.data == "ANIMALS"

        call.data = 'А'
        Hangman.get_callback(call, bot, 0)
        assert call.data == 'А'

        call.data = '🚫️'
        Hangman.get_callback(call, bot, 0)
        assert call.data == '🚫️'


class TestXO_group:
    """
    Класс тестирования Крестиков-ноликов в групповом чате.
    """
    @fix_tooManyRequests_err
    def test_X_win(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)
        call = types.CallbackQuery(1, user, "XO_group", None, message)
        TTT_group.get_callback(call, bot)
        assert call.data == "XO_group"
        call.data = "position1"
        TTT_group.get_callback(call, bot)
        assert call.data == "position1"
        user.id = 2
        call.data = "position0"
        TTT_group.get_callback(call, bot)
        assert call.data == "position0"
        user.id = 1
        call.data = "position4"
        TTT_group.get_callback(call, bot)
        assert call.data == "position4"
        user.id = 2
        call.data = "position3"
        TTT_group.get_callback(call, bot)
        assert call.data == "position3"
        user.id = 1
        call.data = "position7"
        TTT_group.get_callback(call, bot)
        assert call.data == "position7"

    @fix_tooManyRequests_err
    def test_O_win(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)
        call = types.CallbackQuery(1, user, "XO_group", None, message)
        TTT_group.get_callback(call, bot)
        assert call.data == "XO_group"
        call.data = "position1"
        TTT_group.get_callback(call, bot)
        assert call.data == "position1"
        user.id = 2
        call.data = "position0"
        TTT_group.get_callback(call, bot)
        assert call.data == "position0"
        user.id = 1
        call.data = "position4"
        TTT_group.get_callback(call, bot)
        assert call.data == "position4"
        user.id = 2
        call.data = "position3"
        TTT_group.get_callback(call, bot)
        assert call.data == "position3"
        user.id = 1
        call.data = "position2"
        TTT_group.get_callback(call, bot)
        assert call.data == "position2"
        user.id = 2
        call.data = "position6"
        TTT_group.get_callback(call, bot)
        assert call.data == "position6"

    @fix_tooManyRequests_err
    def test_OX_draw(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)
        call = types.CallbackQuery(1, user, "XO_group", None, message)
        TTT_group.get_callback(call, bot)
        assert call.data == "XO_group"
        call.data = "position0"
        TTT_group.get_callback(call, bot)
        assert call.data == "position0"
        user.id = 2
        call.data = "position1"
        TTT_group.get_callback(call, bot)
        assert call.data == "position1"
        user.id = 1
        call.data = "position2"
        TTT_group.get_callback(call, bot)
        assert call.data == "position2"
        user.id = 2
        call.data = "position3"
        TTT_group.get_callback(call, bot)
        assert call.data == "position3"
        user.id = 1
        call.data = "position4"
        TTT_group.get_callback(call, bot)
        assert call.data == "position4"
        user.id = 2
        call.data = "position6"
        TTT_group.get_callback(call, bot)
        assert call.data == "position6"
        user.id = 1
        call.data = "position5"
        TTT_group.get_callback(call, bot)
        assert call.data == "position5"
        user.id = 2
        call.data = "position8"
        TTT_group.get_callback(call, bot)
        assert call.data == "position8"
        user.id = 1
        call.data = "position7"
        TTT_group.get_callback(call, bot)
        assert call.data == "position7"


class TestXO_main:
    """
    Класс тестирования Крестиков-ноликов в личном чате.
    """
    @fix_tooManyRequests_err
    def test_XO_connect(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        message_id_2 = bot.send_message(CHAT_ID_2, 'text').message_id
        assert message_id_2
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "private")
        user = types.User(723229931, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)
        call = types.CallbackQuery(None, user, "XO_start", None, message)
        menu_keyboard = gen_menu_keyboard(call, call.message.chat.type)
        XO_class.xo_lobby_handler(call, bot, menu_keyboard)
        assert call.data == "XO_start"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        XO_class.xo_lobby_handler(call, bot, menu_keyboard)
        assert call.data == "XO_start"
        call.data = "XO_stop"
        XO_class.xo_lobby_handler(call, bot, menu_keyboard)
        assert call.data == "XO_stop"
        chat.id = CHAT_ID
        message.message_id = message_id
        XO_class.xo_lobby_handler(call, bot, menu_keyboard)
        assert call.data == "XO_stop"

    @fix_tooManyRequests_err
    def test_X_group(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        message_id_2 = bot.send_message(CHAT_ID_2, 'text').message_id
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "private")
        user = types.User(723229931, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)
        call = types.CallbackQuery(None, user, "XO_start", None, message)
        menu_keyboard = gen_menu_keyboard(call, call.message.chat.type)
        XO_class.xo_lobby_handler(call, bot, menu_keyboard)
        assert call.data == "XO_start"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        XO_class.xo_lobby_handler(call, bot, menu_keyboard)
        assert call.data == "XO_start"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_0"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_0"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        call.data = "xo_start_3"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_3"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_1"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_1"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        call.data = "xo_start_4"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_4"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_2"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_2"

    @fix_tooManyRequests_err
    def test_0_group(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        message_id_2 = bot.send_message(CHAT_ID_2, 'text').message_id
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "private")
        user = types.User(723229931, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)
        call = types.CallbackQuery(None, user, "XO_start", None, message)
        menu_keyboard = gen_menu_keyboard(call, call.message.chat.type)
        XO_class.xo_lobby_handler(call, bot, menu_keyboard)
        assert call.data == "XO_start"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        XO_class.xo_lobby_handler(call, bot, menu_keyboard)
        assert call.data == "XO_start"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_0"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_0"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        call.data = "xo_start_3"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_3"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_1"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_1"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        call.data = "xo_start_4"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_4"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_6"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_6"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        call.data = "xo_start_5"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_5"

    @fix_tooManyRequests_err
    def test_XO_group(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        message_id_2 = bot.send_message(CHAT_ID_2, 'text').message_id
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "private")
        user = types.User(723229931, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)
        call = types.CallbackQuery(None, user, "XO_start", None, message)
        menu_keyboard = gen_menu_keyboard(call, call.message.chat.type)
        XO_class.xo_lobby_handler(call, bot, menu_keyboard)
        assert call.data == "XO_start"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        XO_class.xo_lobby_handler(call, bot, menu_keyboard)
        assert call.data == "XO_start"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_0"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_0"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        call.data = "xo_start_1"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_1"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_2"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_2"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        call.data = "xo_start_3"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_3"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_4"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_4"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        call.data = "xo_start_6"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_6"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_5"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_5"
        chat.id = CHAT_ID_2
        message.message_id = message_id_2
        call.data = "xo_start_8"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_8"
        chat.id = CHAT_ID
        message.message_id = message_id
        call.data = "xo_start_7"
        XO_class.xo_game_core(call, bot, menu_keyboard)
        assert call.data == "xo_start_7"


class TestSlots:
    """
    Класс тестирования Слотов.
    """
    @fix_tooManyRequests_err
    def test_slots_start(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': "Сообщение"}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'ИМЯ', 'ФАМИЛИЯ', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)

        call = types.CallbackQuery(1, user, "Slots", None, message)
        Slots.callback_inline(call, bot)

    @fix_tooManyRequests_err
    def test_slots_spin(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': "Сообщение"}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'QWE', 'ZXC', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)

        call = types.CallbackQuery(1, user, "spin", None, message)
        Slots.callback_inline(call, bot)


class TestBlackjack:
    """
    Класс тестирования Блекджека.
    """
    @fix_tooManyRequests_err
    def test_card(self):
        card = Card("Ace", "♥")

        assert card.display_card_info() == "♥Ace"

    @fix_tooManyRequests_err
    def test_deck(self):
        deck = Deck()
        deck.pop_card_from_deck()
        deck.shuffle_deck()
        deck.double_deck()

    @fix_tooManyRequests_err
    def test_player(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': "Сообщение"}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'ИМЯ', 'ФАМИЛИЯ', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)

        call = types.CallbackQuery(1, user, "bj_play", None, message)

        game = Player(call.from_user.first_name, call.message.chat.id, 50)
        game.deck.double_deck()
        game.deck.shuffle_deck()
        game.next_round()
        game.lose_the_game()

    @fix_tooManyRequests_err
    def test_blackjack_start(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': "Сообщение"}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'ИМЯ', 'ФАМИЛИЯ', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)

        call = types.CallbackQuery(1, user, "Blackjack", None, message)
        Blackjack.get_callback(call, bot)

    @fix_tooManyRequests_err
    def test_blackjack_play(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': "Сообщение"}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'ИМЯ', 'ФАМИЛИЯ', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)

        call = types.CallbackQuery(1, user, "bj_play", None, message)
        Blackjack.get_callback(call, bot)

    @fix_tooManyRequests_err
    def test_blackjack_take_card(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': "Сообщение"}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'ИМЯ', 'ФАМИЛИЯ', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)

        call = types.CallbackQuery(1, user, "bj_play", None, message)
        Blackjack.get_callback(call, bot)

        call = types.CallbackQuery(1, user, "bj_takeCard", None, message)
        Blackjack.get_callback(call, bot)

    @fix_tooManyRequests_err
    def test_blackjack_do_not_take_card(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': "Сообщение"}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'ИМЯ', 'ФАМИЛИЯ', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)

        call = types.CallbackQuery(1, user, "bj_play", None, message)
        Blackjack.get_callback(call, bot)

        call = types.CallbackQuery(1, user, "bj_doNTCard", None, message)
        Blackjack.get_callback(call, bot)

    @fix_tooManyRequests_err
    def test_blackjack_leave(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': "Сообщение"}
        chat = types.Chat(CHAT_ID, "supergroup")
        user = types.User(1, False, 'ИМЯ', 'ФАМИЛИЯ', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)

        call = types.CallbackQuery(1, user, "bj_play", None, message)
        Blackjack.get_callback(call, bot)

        call = types.CallbackQuery(1, user, "bj_leave", None, message)
        Blackjack.get_callback(call, bot)


class TestTorA:
    """
    Класс тестирования игры Правда или действие
    """
    @fix_tooManyRequests_err
    def test_TorA_action(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "private")
        user = types.User(1, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)
        call = types.CallbackQuery(None, user, None, None, message)
        call.data = "TorA_action"
        TorA_core.main_handler(bot, call)
        assert call.data == "TorA_action"
        call.data = "TorA_start"
        TorA_core.main_handler(bot, call)
        assert call.data == "TorA_start"
        call.data = "TorA_action"
        TorA_core.main_handler(bot, call)
        assert call.data == "TorA_action"
        call.data = "TorA_start"
        TorA_core.main_handler(bot, call)
        assert call.data == "TorA_start"

    @fix_tooManyRequests_err
    def test_TorA_true(self):
        message_id = bot.send_message(CHAT_ID, 'text').message_id
        params = {'text': r'TEST'}
        chat = types.Chat(CHAT_ID, "private")
        user = types.User(1, False, 'ЖЕНЯ', 'КЛОУН', '🤡', 'ru')
        message = types.Message(message_id, user, None, chat, "text", params, None)
        call = types.CallbackQuery(None, user, None, None, message)
        call.data = "TorA_true"
        TorA_core.main_handler(bot, call)
        assert call.data == "TorA_true"
        call.data = "TorA_start"
        TorA_core.main_handler(bot, call)
        assert call.data == "TorA_start"
        call.data = "TorA_true"
        TorA_core.main_handler(bot, call)
        assert call.data == "TorA_true"
        call.data = "TorA_start"
        TorA_core.main_handler(bot, call)
        assert call.data == "TorA_start"
