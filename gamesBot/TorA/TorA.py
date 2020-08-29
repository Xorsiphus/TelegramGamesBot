"""
Игра Правда или Действие.
"""
import random

from telebot import types

from gamesBot import Translation


class TorA_core:
    """
    Классы игры Правда или Действие.
    """
    call_list = ["TorA_start", "TorA_true", "TorA_action"]
    __dictionaries = {"true": {}, "action": {}}
    __last = {}

    @classmethod
    def main_handler(cls, bot, call):
        """
        Метод, обрабатывающий колбеки.

        :param bot: Бот.
        :param call: Колбэк.
        """
        if call.data == 'TorA_start':
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=cls.gen_tora_markup(call.from_user.id),
                                  text=Translation.get_tora_menu_expression("choose", call.from_user.id),
                                  message_id=call.message.message_id)
        elif call.data == 'TorA_true':
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=None, text=call.message.text,
                                  message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id, reply_markup=cls.gen_tora_markup(call.from_user.id),
                             text=cls.get_rand_true(call.from_user.id, call.message.text))
        elif call.data == 'TorA_action':
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=None, text=call.message.text,
                                  message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id, reply_markup=cls.gen_tora_markup(call.from_user.id),
                             text=cls.get_rand_action(call.from_user.id, call.message.text))

    @classmethod
    def get_rand_true(cls, user_id, old_message_text):
        """
        Метод, возвращающий новую "правду".

        :param user_id: ID пользователя.
        :param old_message_text: текст старого сообщения.
        :return: Новая фраза с "правдой"
        """
        if user_id not in cls.__dictionaries['true'] or cls.__dictionaries['true'][user_id] == []:
            cls.__dictionaries['true'][user_id] = Translation.get_tora_true_dict()
        key = random.randint(0, len(cls.__dictionaries['true'][user_id]) - 1)
        while old_message_text in cls.__dictionaries['true'][user_id][key]:
            key = random.randint(0, len(cls.__dictionaries['true'][user_id]) - 1)
        return cls.__dictionaries['true'][user_id].pop(key)[Translation.get_player_language(user_id)]

    @classmethod
    def get_rand_action(cls, user_id, old_message_text):
        """
        Метод, возвращающий новое "действие".

        :param user_id: ID пользователя.
        :param old_message_text: текст старого сообщения.
        :return: Новая фраза с "действием"
        """
        if user_id not in cls.__dictionaries['action'] or cls.__dictionaries['action'][user_id] == []:
            cls.__dictionaries['action'][user_id] = Translation.get_tora_action_dict()
        key = random.randint(0, len(cls.__dictionaries['action'][user_id]) - 1)
        while old_message_text in cls.__dictionaries['action'][user_id][key]:
            key = random.randint(0, len(cls.__dictionaries['action'][user_id]) - 1)
        return cls.__dictionaries['action'][user_id].pop(key)[Translation.get_player_language(user_id)]

    @staticmethod
    def gen_tora_markup(user_id):
        """
        Метод, генерирующий клвиатуру-меню.

        :param user_id: ID пользователя.
        :return: Клавиатура-меню для игры.
        """
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        b1 = types.InlineKeyboardButton(text=Translation.get_tora_menu_expression(key="true", user_id=user_id),
                                        callback_data="TorA_true")
        b2 = types.InlineKeyboardButton(text=Translation.get_tora_menu_expression(key="action", user_id=user_id),
                                        callback_data="TorA_action")
        b3 = types.InlineKeyboardButton(text=Translation.get_tora_menu_expression(key="exit", user_id=user_id),
                                        callback_data="Menu")

        keyboard.add(b1, b2)
        keyboard.add(b3)

        return keyboard
