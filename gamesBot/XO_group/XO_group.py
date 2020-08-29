"""
Игра Крастики-Нолики (групп. чат).
"""
from telebot import types
# Библеотека класс переводчика
from gamesBot import Translation


class TTT_group:
    """
    Классы игры Крестики-Нолики.
    """
    players = []
    values = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    call_list = ["XO_group", "position0", "position1", "position2", "position3", "position4",
                 "position5", "position6", "position7", "position8"]

    @classmethod
    def main_slots(cls, call, bot):
        """
        Метод, запускающий новую игру

        :param call: Колбэк
        :param bot: Бот
        """
        tmp_player = cls.player_founder(call)
        tmp_player[1] = list(cls.values)
        tmp_player[2] = 0
        tmp_player[3] = 0
        # Сообщение + Кнопка для игры в "Слоты"
        # if message.text == "Play \"Slots\"" or message.text == "Играть в \"Слоты\"":
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        button = []
        for i in range(0, 9):
            button.append(types.InlineKeyboardButton(" ", callback_data='position' + str(i)))
        button.append(types.InlineKeyboardButton(
            Translation.get_menu_expression("exit", call.from_user.id), callback_data='Menu'))
        keyboard.add(*button)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              reply_markup=keyboard,
                              text="❌⭕️",
                              message_id=call.message.message_id)

    # Найти игрока по ID
    @classmethod
    def player_founder(cls, call):
        """
        Метод, находящий игрока в списе игроков по ID

        :param call: Колбек
        :return: Игрок
        """
        while True:
            for player in cls.players:
                if player[0] == call.message.chat.id:
                    return player
            cls.players.append([call.message.chat.id, list(cls.values), 0, 0])

    @classmethod
    def get_callback(cls, call, bot):
        """
        Метод, обрабатывающий колбэки

        :param call: Колбэк
        :param bot: Бот
        """
        tmp_player = cls.player_founder(call)
        if call.data == 'XO_group':
            cls.main_slots(call, bot)
            return
        if call.from_user.id == tmp_player[3]:
            return
        for i in range(0, 9):
            if call.data == "position" + str(i):
                tmp_player[3] = call.from_user.id
                markup = types.InlineKeyboardMarkup(row_width=3)
                button = []
                for value in range(0, 9):
                    if value == i:
                        if tmp_player[2] % 2 == 0:
                            button.append(types.InlineKeyboardButton('X', callback_data='position' + str(value)))
                            tmp_player[1][value] = 'X'
                        else:
                            button.append(types.InlineKeyboardButton('0', callback_data='position' + str(value)))
                            tmp_player[1][value] = '0'
                        tmp_player[2] += 1
                    else:
                        button.append(types.InlineKeyboardButton(tmp_player[1][value],
                                                                 callback_data='position' + str(value)))
                button.append(types.InlineKeyboardButton(
                    Translation.get_menu_expression("exit", call.from_user.id), callback_data='Menu'))
                markup.add(*button)
                bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=markup, text=call.message.text,
                                      message_id=call.message.message_id)
                if " " not in tmp_player[1]:
                    keyboard = types.InlineKeyboardMarkup()
                    again = types.InlineKeyboardButton(
                        Translation.get_hangman_exp("play_again", call.from_user.id), callback_data='XO_group')
                    ex = types.InlineKeyboardButton(
                        Translation.get_menu_expression("exit", call.from_user.id), callback_data='Menu')
                    keyboard.add(again, ex)
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          reply_markup=keyboard,
                                          text="Ничья",
                                          message_id=call.message.message_id)
                if tmp_player[1][0] == tmp_player[1][1] == tmp_player[1][2] != " " or tmp_player[1][3] == \
                        tmp_player[1][4] == tmp_player[1][5] != " " or \
                        tmp_player[1][6] == tmp_player[1][7] == tmp_player[1][8] != " " or tmp_player[1][0] == \
                        tmp_player[1][3] == tmp_player[1][6] != " " or \
                        tmp_player[1][1] == tmp_player[1][4] == tmp_player[1][7] != " " or tmp_player[1][2] == \
                        tmp_player[1][5] == tmp_player[1][8] != " " or tmp_player[1][0] == tmp_player[1][4] == \
                        tmp_player[1][8] != " " or tmp_player[1][2] == tmp_player[1][4] == tmp_player[1][6] != " ":
                    if tmp_player[2] % 2 == 0:
                        text = '⭕'
                    else:
                        text = '❌'
                    keyboard = types.InlineKeyboardMarkup()
                    again = types.InlineKeyboardButton(
                        Translation.get_hangman_exp("play_again", call.from_user.id), callback_data='XO_group')
                    ex = types.InlineKeyboardButton(
                        Translation.get_menu_expression("exit", call.from_user.id), callback_data='Menu')
                    keyboard.add(again, ex)
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          reply_markup=keyboard,
                                          text=text + " - Выиграл",
                                          message_id=call.message.message_id)
