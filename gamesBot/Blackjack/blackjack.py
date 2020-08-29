"""
Игра Блекджек.
"""
from . import Player
from gamesBot import Translation

from telebot import types

ID = 0


class Blackjack:
    """
    Класс игры Блекджек.
    """
    call_list = ["Blackjack", "bj_play", "bj_takeCard", 'bj_doNTCard', "bj_leave"]

    __players = []

    @classmethod
    def get_callback(cls, call, bot):
        """
        Метод, обрабатывающий колбеки.

        :param call: Колбек.
        :param bot: Бот.
        """
        cls.__flag = True
        if call.data == 'Blackjack':
            cls.handle_menu(call, bot)
        elif call.data == 'bj_play':
            cls.handle_play_blackjack(call, bot)
        elif 'bj_takeCard' == call.data:
            cls.handle_take_card(call, bot)
        elif 'bj_doNTCard' == call.data:
            cls.handle_do_not_take_anymore(call, bot)
        elif 'bj_leave' == call.data:
            cls.handle_leave_game(call, bot)

    @staticmethod
    def gen_menu_keyboard(user_id):
        """
        Метод, генерирующий главное меню игры Блекджек.

        :param user_id: ID юзера.
        :return: Сгенерированная клавиатура.
        """
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        b1 = types.InlineKeyboardButton(Translation.get_bj_expression("Play Blackjack!", user_id),
                                        callback_data='bj_play')
        b2 = types.InlineKeyboardButton(Translation.get_bj_expression("Menu", user_id),
                                        callback_data='Menu')
        keyboard.add(b1)
        keyboard.add(b2)

        return keyboard

    @staticmethod
    def gen_game_blackjack_keyboard(user_id):
        """
        Метод, генерирующий меню для игры в Блекджек.

        :param user_id: ID юзера.
        :return: Сгенерированная клавиатура.
        """
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        b1 = types.InlineKeyboardButton(Translation.get_bj_expression("TakeCard", user_id),
                                        callback_data='bj_takeCard')
        b2 = types.InlineKeyboardButton(Translation.get_bj_expression("DoNotTakeCard", user_id),
                                        callback_data='bj_doNTCard')
        b3 = types.InlineKeyboardButton(Translation.get_bj_expression("LeaveBlackjack", user_id),
                                        callback_data='bj_leave')
        keyboard.add(b1)
        keyboard.add(b2)
        keyboard.add(b3)

        return keyboard

    @classmethod
    def checker(cls, player_id):
        """
        Метод, который проверяет, существует ли игрок.

        :param player_id: ID игрока.
        :return: True, если существует, иначе False.
        """
        for game in cls.__players:
            if player_id == game.telegram_id:
                return True
        return False

    @classmethod
    def id_found(cls, call):
        """
        Метод, который ищет игрока по ID.

        :param call: Колбек.
        """
        while True:
            for game in cls.__players:
                if game.telegram_id == call.message.chat.id:
                    return game
            game = Player(call.from_user.first_name, call.message.chat.id, 50)
            game.deck.double_deck()
            game.deck.shuffle_deck()
            game.next_round()
            game.lose_the_game()
            cls.__players.append(game)

    @classmethod
    def handle_menu(cls, call, bot):
        """
        Метод, который обрабатывает колбек 'Blackjack'.

        :param call: Колбек.
        :param bot: Бот.
        """
        keyboard = cls.gen_menu_keyboard(call.from_user.id)
        bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                              text=Translation.get_bj_expression("Blackjack",
                                                                 Translation.get_player_language(call.from_user.id)),
                              message_id=call.message.message_id)

    @classmethod
    def handle_play_blackjack(cls, call, bot):
        """
        Метод, который обрабатывает колбек 'bj_play'.

        :param call: Колбек.
        :param bot: Бот.
        """
        if cls.checker(call.message.chat.id):
            cls.__players.remove(cls.id_found(call))

        game = Player(call.from_user.first_name, call.message.chat.id, 50)
        game.deck.double_deck()
        game.deck.shuffle_deck()
        game.next_round()
        cls.__players.append(game)

        if game.stop_the_game:
            keyboard = cls.gen_menu_keyboard(call.from_user.id)
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                  text=game.display_result(Translation.get_player_language(call.from_user.id)),
                                  message_id=call.message.message_id)
            cls.__players.remove(game)
        else:
            msg = game.display_first_round(Translation.get_player_language(call.from_user.id))
            keyboard = cls.gen_game_blackjack_keyboard(call.from_user.id)
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                  text=msg,
                                  message_id=call.message.message_id)

    @classmethod
    def handle_take_card(cls, call, bot):
        """
        Метод, который обрабатывает колбек 'bj_takeCard'.

        :param call: Колбек.
        :param bot: Бот.
        """
        if cls.checker(call.message.chat.id):
            cls.id_found(call).next_round()

            player_round_message = cls.id_found(call).display_player_round(
                Translation.get_player_language(call.from_user.id))
            keyboard = cls.gen_game_blackjack_keyboard(call.from_user.id)
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                  text=player_round_message,
                                  message_id=call.message.message_id)

            if cls.id_found(call).stop_the_game:
                keyboard = cls.gen_menu_keyboard(call.from_user.id)
                bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                      text=cls.id_found(call).display_result(
                                          Translation.get_player_language(call.from_user.id)),
                                      message_id=call.message.message_id)
                cls.__players.remove(cls.id_found(call))
        else:
            cls.handle_menu(call, bot)

    @classmethod
    def handle_do_not_take_anymore(cls, call, bot):
        """
        Метод, который обрабатывает колбек 'bj_doNTCard'.

        :param call: Колбек.
        :param bot: Бот.
        """
        if cls.checker(call.message.chat.id):
            cls.id_found(call).is_player_active = False

            if cls.checker(call.message.chat.id):
                while cls.id_found(call).stop_the_game is not True:
                    cls.id_found(call).next_round()

                keyboard = cls.gen_menu_keyboard(call.from_user.id)
                bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                      text=cls.id_found(call).display_result(
                                          Translation.get_player_language(call.from_user.id)),
                                      message_id=call.message.message_id)
                cls.__players.remove(cls.id_found(call))
        else:
            cls.handle_menu(call, bot)

    @classmethod
    def handle_leave_game(cls, call, bot):
        """
        Метод, который обрабатывает колбек 'bj_leave'.

        :param call: Колбек.
        :param bot: Бот.
        """
        if cls.checker(call.message.chat.id):
            cls.__players.remove(cls.id_found(call))
        cls.handle_menu(call, bot)
