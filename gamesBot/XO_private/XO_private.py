"""
Игра Крастики-Нолики(coop).
"""
from time import sleep

from gamesBot import Translation

from telebot import types

import re

from functools import reduce

from gamesBot import gen_menu_keyboard


class XO_class:
    """
    Классы игры Крестики-Нолики.
    """
    call_list = ["XO_start", "XO_stop", "XO_start", "xo_start_0", "xo_start_1", "xo_start_2", "xo_start_3",
                 "xo_start_4", "xo_start_5", "xo_start_6", "xo_start_7", "xo_start_8"]

    mark = {0: " ", 1: "❌", 2: "⭕️"}

    __players = {}
    __sessions = {}
    __marks = {}
    __move = {}
    __game_message_id = {}

    @classmethod
    def xo_lobby_handler(cls, call, bot, menu_keyboard):
        """
        Метод, обрабатывающий колбэки.

        :param call: Колбэк.
        :param bot: Бот.
        :param menu_keyboard: Разметка прикрепляемой клавиатуры-меню.
        """

        if call.message.chat.type == "private":
            if len(cls.__players) % 2 == 1 and cls.__players.get(call.message.chat.id, -1) == -1:
                if call.data == "XO_start":
                    second_id = cls.get_waiting_player(call)
                    cls.__game_message_id[call.message.chat.id] = call.message.message_id

                    bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=cls.gen_exit_markup(call.message.chat.id),
                                          text=Translation.get_xo_menu_expression("connection msg for P2",
                                                                                  call.message.chat.id),
                                          message_id=call.message.message_id)
                    bot.edit_message_text(chat_id=second_id, reply_markup=cls.gen_exit_markup(second_id),
                                          text=Translation.get_xo_menu_expression("connection msg for P1", second_id),
                                          message_id=cls.__game_message_id[second_id])
                    print(Translation.get_xo_log_expression("log - connection").format(call.message.chat.id, second_id))

                    sleep(2)
                    cls.xo_game_start(call, bot)

            elif len(cls.__players) % 2 == 0:
                if call.data == "XO_start" and cls.__players.get(call.message.chat.id, -1) == -1:
                    cls.__players[call.message.chat.id] = 0
                    cls.__game_message_id[call.message.chat.id] = call.message.message_id

                    bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=cls.gen_exit_markup(call.message.chat.id),
                                          text=Translation.get_xo_menu_expression("man for P1", call.message.chat.id),
                                          message_id=call.message.message_id)
                    print(Translation.get_xo_log_expression("log - 1/2").format(call.message.chat.id))

            if call.data == "XO_stop":
                if XO_class.check_id_in_lobby_dict(call.message.chat.id, call.message.chat.type):
                    XO_class.stopper(call.message.chat.id, bot, menu_keyboard, True)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=menu_keyboard,
                                          text=Translation.get_xo_menu_expression("disconnect msg for P2",
                                                                                  call.message.chat.id),
                                          message_id=cls.__game_message_id[call.message.chat.id])

            if call.data == "XO_start":
                print(cls.__players)

    @classmethod
    def stopper(cls, first_id, bot, menu_keyboard, message_flag):
        """
        Метод, останавливающий игру и очищающий переменные.

        :param first_id: ID первого пользователя.
        :param bot: Бот.
        :param menu_keyboard: Разметка прикрепляемой клавиатуры-меню.
        :param message_flag: Пометка.
        """
        try:
            second_id = cls.__players[first_id]
        except Exception as err:
            print(Translation.get_xo_log_expression("log - del error").format(err))
            print(cls.__players)
            return

        if message_flag:
            try:
                bot.edit_message_text(chat_id=second_id, reply_markup=menu_keyboard,
                                      text=Translation.get_xo_menu_expression("disconnect msg for P1", second_id),
                                      message_id=cls.__game_message_id[second_id])
            except Exception as err:
                print(Translation.get_xo_log_expression("msg send error").format(err))
            try:
                bot.edit_message_text(chat_id=first_id, reply_markup=menu_keyboard,
                                      text=Translation.get_xo_menu_expression("disconnect msg for P2", first_id),
                                      message_id=cls.__game_message_id[first_id])
            except Exception as err:
                print(Translation.get_xo_log_expression("msg send error").format(err))

        if second_id != 0:
            cls.__move[first_id + second_id] = -1

        try:
            del cls.__players[second_id]
        except Exception as err:
            print(Translation.get_xo_log_expression("miss player").format(err))
        try:
            del cls.__players[first_id]
        except Exception as err:
            print(Translation.get_xo_log_expression("miss player").format(err))

        print(Translation.get_xo_log_expression("log - del lobby").format(first_id, second_id))
        print(cls.__players)

        if len(cls.__players) == 0:
            cls.__players = {}

    @classmethod
    def get_waiting_player(cls, call):
        """
        Метод, получающий ID ожидающего игрока.

        :param call: Колбэк.
        :return: ID ожидающего игрока.
        """
        target_id = 0

        for i in cls.__players:
            if cls.__players[i] == 0:
                target_id = i
        cls.__players[call.message.chat.id] = target_id
        cls.__players[target_id] = call.message.chat.id

        return target_id

    @classmethod
    def check_id_in_lobby_dict(cls, user_id, chat_type):
        """
        Метод, проверяющий игрока на наличие в лобби.

        :param user_id: ID пользователя.
        :param chat_type: Тип чата.
        :return: Логическое значение(Наличие игрока в лобби).
        """
        if chat_type == "private":
            if user_id in cls.__players:
                return 1
            else:
                return 0

    @classmethod
    def xo_game_start(cls, call, bot):
        """
        Метод, запускающий игру, после создания лобби.

        :param call: Колбэк.
        :param bot: Бот.
        """
        markup = types.InlineKeyboardMarkup(row_width=3)
        b1 = types.InlineKeyboardButton(" ", callback_data='xo_start_0')
        b2 = types.InlineKeyboardButton(" ", callback_data='xo_start_1')
        b3 = types.InlineKeyboardButton(" ", callback_data='xo_start_2')
        b4 = types.InlineKeyboardButton(" ", callback_data='xo_start_3')
        b5 = types.InlineKeyboardButton(" ", callback_data='xo_start_4')
        b6 = types.InlineKeyboardButton(" ", callback_data='xo_start_5')
        b7 = types.InlineKeyboardButton(" ", callback_data='xo_start_6')
        b8 = types.InlineKeyboardButton(" ", callback_data='xo_start_7')
        b9 = types.InlineKeyboardButton(" ", callback_data='xo_start_8')
        markup.add(b1, b2, b3, b4, b5, b6, b7, b8, b9)
        markup.add(types.InlineKeyboardButton("Exit", callback_data='XO_stop'))
        cls.__sessions[call.message.chat.id + cls.__players[call.message.chat.id]] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        cls.__marks[call.message.chat.id] = 2
        cls.__marks[cls.__players[call.message.chat.id]] = 1
        bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=markup,
                              text=Translation.get_xo_menu_expression("public move msg", call.message.chat.id),
                              message_id=cls.__game_message_id[call.message.chat.id])
        bot.edit_message_text(chat_id=cls.__players[call.message.chat.id], reply_markup=markup,
                              text=Translation.get_xo_menu_expression("public move msg",
                                                                      cls.__players[call.message.chat.id]),
                              message_id=cls.__game_message_id[cls.__players[call.message.chat.id]])

    @classmethod
    def xo_game_core(cls, call, bot, menu_keyboard):
        """
        Метод, обрабатывающий игровые события.

        :param call: Колбэк.
        :param bot: Бот.
        :param menu_keyboard: Разметка прикрепляемой клавиатуры-меню.
        """
        if call.data[0:8] == "xo_start":
            first_id = call.message.chat.id
            try:
                second_id = cls.__players[call.message.chat.id]
            except Exception as err:
                print(Translation.get_xo_log_expression("log - old cb").format(err))
                return

            if cls.__move.get(first_id + second_id, -1) == -1:
                cls.__move[first_id + second_id] = first_id

            if cls.__move[first_id + second_id] == second_id:
                return

            pos = int(re.findall("\d+", call.data)[0])
            try:
                session = cls.__sessions[first_id + second_id]
            except Exception as err:
                print(Translation.get_xo_log_expression("log - miss session").format(err))
                return
            if session[pos] == 0:
                session[pos] = cls.__marks[first_id]

                winner = XO_class.victory_checker(first_id + second_id)
                if winner == "error":
                    return
                elif winner == "draw":
                    XO_class.stopper(first_id, bot, menu_keyboard, False)
                    end_board = cls.game_over_message_generator(session)

                    bot.edit_message_text(chat_id=first_id, reply_markup=None,
                                          text=Translation.get_xo_menu_expression("draw", user_id=first_id) + end_board,
                                          message_id=cls.__game_message_id[first_id])
                    bot.send_message(first_id,
                                     Translation.get_menu_expression("choose_game", user_id=first_id),
                                     reply_markup=gen_menu_keyboard(first_id, 'private'))

                    bot.edit_message_text(chat_id=second_id, reply_markup=None,
                                          text=Translation.get_xo_menu_expression("draw",
                                                                                  user_id=second_id) + end_board,
                                          message_id=cls.__game_message_id[second_id])
                    bot.send_message(second_id,
                                     Translation.get_menu_expression("choose_game", user_id=second_id),
                                     reply_markup=gen_menu_keyboard(second_id, 'private'))
                    return
                elif winner == "victory":
                    XO_class.stopper(first_id, bot, menu_keyboard, False)
                    end_board = cls.game_over_message_generator(session)

                    bot.edit_message_text(chat_id=first_id, reply_markup=None,
                                          text=Translation.get_xo_menu_expression("win", user_id=first_id) + end_board,
                                          message_id=cls.__game_message_id[first_id])
                    bot.send_message(first_id,
                                     Translation.get_menu_expression("choose_game", user_id=first_id),
                                     reply_markup=gen_menu_keyboard(first_id, 'private'))
                    if call.id:
                        bot.answer_callback_query(callback_query_id=call.id,
                                                   text=Translation.get_xo_menu_expression("win", user_id=first_id),
                                                   show_alert=True)

                    bot.edit_message_text(chat_id=second_id, reply_markup=None,
                                          text=Translation.get_xo_menu_expression("lose",
                                                                                  user_id=second_id) + end_board,
                                          message_id=cls.__game_message_id[second_id])
                    bot.send_message(second_id,
                                     Translation.get_menu_expression("choose_game", user_id=second_id),
                                     reply_markup=gen_menu_keyboard(second_id, 'private'))
                    return

                markup = types.InlineKeyboardMarkup(row_width=3)
                b1 = types.InlineKeyboardButton(cls.mark[session[0]], callback_data='xo_start_0')
                b2 = types.InlineKeyboardButton(cls.mark[session[1]], callback_data='xo_start_1')
                b3 = types.InlineKeyboardButton(cls.mark[session[2]], callback_data='xo_start_2')
                b4 = types.InlineKeyboardButton(cls.mark[session[3]], callback_data='xo_start_3')
                b5 = types.InlineKeyboardButton(cls.mark[session[4]], callback_data='xo_start_4')
                b6 = types.InlineKeyboardButton(cls.mark[session[5]], callback_data='xo_start_5')
                b7 = types.InlineKeyboardButton(cls.mark[session[6]], callback_data='xo_start_6')
                b8 = types.InlineKeyboardButton(cls.mark[session[7]], callback_data='xo_start_7')
                b9 = types.InlineKeyboardButton(cls.mark[session[8]], callback_data='xo_start_8')
                markup.add(b1, b2, b3, b4, b5, b6, b7, b8, b9)
                markup.add(types.InlineKeyboardButton("Exit", callback_data='XO_stop'))
                cls.__move[first_id + second_id] = second_id
                bot.edit_message_text(chat_id=first_id, reply_markup=markup,
                                      text=Translation.get_xo_menu_expression("waiting vic", first_id),
                                      message_id=cls.__game_message_id[first_id])
                bot.edit_message_text(chat_id=second_id, reply_markup=markup,
                                      text=Translation.get_xo_menu_expression("your move msg", second_id),
                                      message_id=cls.__game_message_id[second_id])

    @classmethod
    def victory_checker(cls, target_id):
        """
        Метод, проверяющий поле на конец игры.

        :param target_id: ID-цель пользователя.
        :return: Исход игры.
        """
        try:
            session = cls.__sessions[target_id]
        except Exception as err:
            print(Translation.get_xo_log_expression("log - miss session").format(err))
            return "error"

        victory_numbers = [1, 8]

        if session[0] * session[1] * session[2] in victory_numbers or session[3] * session[4] * session[5] \
                in victory_numbers or session[6] * session[7] * session[8] in victory_numbers or \
                session[0] * session[3] * session[6] in victory_numbers or session[1] * session[4] * \
                session[7] in victory_numbers or session[2] * session[5] * session[8] in victory_numbers or \
                session[0] * session[4] * session[8] in victory_numbers or session[2] * session[4] * session[6] \
                in victory_numbers:
            return "victory"
        elif reduce(lambda x, y: x * y, session) != 0:
            return "draw"
        else:
            return "nothing"

    @classmethod
    def game_over_message_generator(cls, session):
        """
        Метод, генерирующий сообщение об окончании игры.

        :param session: Игровое поле.
        :return: Сообщение об окончании игры.
        """

        field = ''
        lines = 0

        for i in session:
            lines += 1
            if i == 1:
                field += '❌'
                if lines % 3 == 1 or lines % 3 == 2:
                    field += '|'
            elif i == 2:
                field += '⭕️'
                if lines % 3 == 1 or lines % 3 == 2:
                    field += '|'
            else:
                field += '      '
                if lines % 3 == 1 or lines % 3 == 2:
                    field += '|'
            if lines % 3 == 0 and lines < 7:
                field += '\n-------------------\n'
        return field

    @staticmethod
    def gen_exit_markup(user_id):
        """
        Метод, возвращающий клавиатуру-меню для выхода.

        :return: Клавиатура-меню для выхода.
        """
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(Translation.get_xo_menu_expression("stop", user_id), callback_data='XO_stop'))
        return markup
