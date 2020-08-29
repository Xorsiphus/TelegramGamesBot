"""
Игра Виселица.
"""
from telebot import types
# Подключаем модуль случайных чисел
import random
# Импортируем библиотеку для работы с .json файлами
import json

from gamesBot import if_heroku
import os

ID = 0
HP = 1
WORD = 2
GUESS = 3
LETTERS = 4
THEME = 5

if os.path.basename(os.getcwd()) == 'docs':
    TRANSLATION_PATH = f'../gamesBot/Translations/hangman.json'
    CATEGORIES_PATH = f'../gamesBot/Hangman/categories.json'
else:
    TRANSLATION_PATH = f'{if_heroku}Translations/hangman.json'
    CATEGORIES_PATH = f'{if_heroku}Hangman/categories.json'


with open(TRANSLATION_PATH, "r", encoding="utf8") as read:
    translations_HM = json.load(read)

with open(CATEGORIES_PATH, "r", encoding="utf8") as read:
    json_categories = json.load(read)

# Телеграм ID Кирилла
MY_ID = 723229931

# Бкувы для кнопок
ABC = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
ABC_RU = 'А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я'.split() + [' ']
# Список с активными игроками
SWITCHER = {0: 1, 1: 0}
CATEGORIES = ["ALL", "ANIMALS", "EAT", "HOUSE", "CLOTHES", "SCHOOL",
              "MUSIC", "PROFESSIONS", "PC", "NATURE", "SPORT", "BODY"]


class Hangman:
    """
    Класс игры Виселица.
    """
    players = []

    call_list = CATEGORIES + ABC_RU + ABC + ["Hangman", "language_ru", "language_en", "🚫️", "⬇️"]

    @classmethod
    def get_callback(cls, call, bot, lang):
        """
        Метод, обрабатывающий колбеки.

        :param call: Колбек
        :param bot: Бот
        :param lang: Язык
        """
        cls.__flag = True
        tmp_player = cls.player_founder(call.message)
        if call.data == "Hangman":
            if tmp_player[HP] <= 0:
                # Создаём кнопки
                keyboard = cls.create_keyboard(lang)
                cls.menu_btn_add(keyboard, lang)

                bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                      text=translations_HM["categories"][lang],
                                      message_id=call.message.message_id)
            else:
                cls.hp_visual(call, bot, tmp_player,
                              translations_HM["still_going"][lang], lang)
        elif call.data in CATEGORIES:
            if call.data == "ALL":
                call.data = random.choice(list(CATEGORIES[1:]))
            if tmp_player[HP] <= 0:
                cls.new_player(call, bot, tmp_player, lang)
            else:
                cls.hp_visual(call, bot, tmp_player,
                              translations_HM["still_going"][lang], lang)
        elif call.data == "language_ru":
            if lang == 0:
                keyboard = cls.create_keyboard(lang)
                cls.menu_btn_add(keyboard, lang)
                bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                      text=translations_HM["categories"][lang],
                                      message_id=call.message.message_id)
                tmp_player[HP] = 0
            else:
                lang = SWITCHER[lang]
                keyboard = cls.create_keyboard(lang)
                lang = SWITCHER[lang]
                cls.menu_btn_add(keyboard, lang)

                bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                      text=translations_HM["categories"][lang],
                                      message_id=call.message.message_id)
                tmp_player[HP] = -1
        elif call.data == "language_en":
            if lang == 1:
                keyboard = cls.create_keyboard(lang)
                cls.menu_btn_add(keyboard, lang)
                bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                      text=translations_HM["categories"][lang],
                                      message_id=call.message.message_id)
                tmp_player[HP] = 0
            else:
                lang = SWITCHER[lang]
                keyboard = cls.create_keyboard(lang)
                lang = SWITCHER[lang]
                cls.menu_btn_add(keyboard, lang)

                bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                      text=translations_HM["categories"][lang],
                                      message_id=call.message.message_id)
                tmp_player[HP] = -1
        elif call.data in tmp_player[LETTERS]:
            # Находи нашего игрока в списке players
            # Убрать букву
            for i in range(0, len(tmp_player[LETTERS]) - 1):
                if tmp_player[LETTERS][i] == call.data:
                    tmp_player[LETTERS][i] = ' '
            print(tmp_player[WORD])
            # Если игрок угадал
            if str(call.data) in tmp_player[WORD]:
                cls.guess_changer(str(call.data), tmp_player)
                if tmp_player[WORD] == tmp_player[GUESS]:
                    tmp_player[HP] = 0
                    keyboard = cls.end_keyboard(lang)
                    text = translations_HM["you_win"][lang] + ''.join(
                        tmp_player[WORD])
                    bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                          text=text, message_id=call.message.message_id)
                    cls.info(" - Победа!", bot, call, MY_ID)
                else:
                    cls.hp_visual(call, bot, tmp_player, "", lang)
            # Если игрок ошибся
            else:
                # Если проиграл
                if tmp_player[HP] <= 1:
                    tmp_player[HP] = 0
                    keyboard = cls.end_keyboard(lang)
                    text = translations_HM["you_lose"][lang] + \
                           ''.join(tmp_player[WORD])
                    bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                          text=text, message_id=call.message.message_id)
                    cls.info(" - Поражение.", bot, call, MY_ID)
                else:
                    tmp_player[HP] -= 1
                    cls.hp_visual(call, bot, tmp_player, "", lang)
        elif call.data == "🚫️":
            tmp_player[HP] = 0
            keyboard = cls.end_keyboard(lang)
            text = translations_HM["end_message"][lang]
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard,
                                  text=text, message_id=call.message.message_id)
            cls.info(" - Выход.", bot, call.message, MY_ID)
        elif call.data == "⬇️":
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=None,
                                  text="⬇️", message_id=call.message.message_id)
            cls.hp_visual(call, bot, tmp_player, "", lang)

    @staticmethod
    def create_keyboard(lang):
        """
        Метотд, создающий меню с выбором темы

        :param lang: Язык
        :return: Клавиатура
        """
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        # Кнопки с категориями
        categories_words = [
            types.InlineKeyboardButton(text=translations_HM["ALL"][lang], callback_data="ALL"),
            types.InlineKeyboardButton(text=translations_HM["ANIMALS"][lang], callback_data="ANIMALS"),
            types.InlineKeyboardButton(text=translations_HM["EAT"][lang], callback_data="EAT"),
            types.InlineKeyboardButton(text=translations_HM["HOUSE"][lang], callback_data="HOUSE"),
            types.InlineKeyboardButton(text=translations_HM["CLOTHES"][lang], callback_data="CLOTHES"),
            types.InlineKeyboardButton(text=translations_HM["SCHOOL"][lang], callback_data="SCHOOL"),
            types.InlineKeyboardButton(text=translations_HM["MUSIC"][lang], callback_data="MUSIC"),
            types.InlineKeyboardButton(text=translations_HM["BODY"][lang], callback_data="BODY"),
            types.InlineKeyboardButton(text=translations_HM["SPORT"][lang], callback_data="SPORT"),
            types.InlineKeyboardButton(text=translations_HM["PC"][lang], callback_data="PC"),
            types.InlineKeyboardButton(text=translations_HM["NATURE"][lang], callback_data="NATURE"),
            types.InlineKeyboardButton(text=translations_HM["PROFESSIONS"][lang], callback_data="PROFESSIONS")]

        if lang == 1:
            ru = types.InlineKeyboardButton(text=translations_HM["ru"][lang], callback_data="language_ru")
            en = types.InlineKeyboardButton(text=translations_HM["en"][lang], callback_data="none")
        else:
            en = types.InlineKeyboardButton(text=translations_HM["en"][lang], callback_data="language_en")
            ru = types.InlineKeyboardButton(text=translations_HM["ru"][lang], callback_data="none")

        keyboard.add(*categories_words, ru, en)

        return keyboard

    @staticmethod
    def menu_btn_add(keyboard, lang):
        """
        Метод, добавляющий кнопку выхода в главное меню

        :param keyboard: Меню
        :param lang: Язык
        """
        go_menu = types.InlineKeyboardButton(text=translations_HM["Menu"][lang], callback_data="Menu")
        keyboard.add(go_menu)

    @classmethod
    def new_player(cls, call, bot, player, lang):
        """
        Метод, создающий новую игру для игрока

        :param call: Колбек
        :param bot: Бот
        :param player: Игрок
        :param lang: Язык
        """
        # ID - 0, HP - 1, WORD - 2, GUESS - 3, LETTERS - 4, THEME - 5

        player[THEME] = translations_HM[call.data][lang]
        if call.message.json["reply_markup"]["inline_keyboard"][6][0]["callback_data"] == "none":
            player[LETTERS] = list(ABC_RU)
            player[WORD] = list(random.choice(json_categories[call.data][0]))
            player[THEME] += " (RU)"
        else:
            player[LETTERS] = list(ABC)
            player[WORD] = list(random.choice(json_categories[call.data][1]))
            player[THEME] += " (EN)"

        player[HP] = 6
        player[GUESS] = []

        for i in range(0, len(player[WORD])):
            if player[WORD][i] == '-':
                player[GUESS].append("-")
                player[WORD][i] = '-'
            if player[WORD][i] == '_':
                player[GUESS].append(" ")
                player[WORD][i] = ' '
            else:
                player[GUESS].append("_")

        cls.hp_visual(call, bot, player, "", lang)
        if not MY_ID == call.from_user.id:
            bot.send_message(MY_ID, "👁‍🗨 Тема: " + player[THEME])
            bot.send_message(MY_ID, '👁‍🗨 Слово: ' + ''.join(player[WORD]))
            print('Слово: ' + ''.join(player[WORD]))
            bot.send_message(MY_ID, '👁‍🗨 user_id: ' +
                             str(call.from_user.id))
            cls.info("", bot, call, MY_ID)

    # Найти игрока по ID
    @classmethod
    def player_founder(cls, message):
        """
        Метод, находящий игрока в списке игроков по его сообщению

        :param message: Сообщение
        :return: Игрок
        """
        while True:
            for player in cls.players:
                if player[ID] == message.chat.id:
                    return player
            cls.players.append([message.chat.id, 0, [], [], [], ""])

    # <3
    @classmethod
    def hp_visual(cls, call, bot, tmp_player, text, lang):
        """
        Метод, выводящий сообщение с текущим состоянием игры

        :param call: Колбек
        :param bot: Бот
        :param tmp_player: Игрок
        :param text: Доп информация
        :param lang: Язык
        """
        hp = tmp_player[HP]
        tmp = text + translations_HM["theme"][lang] + tmp_player[THEME] + '\n\n'

        if hp > 0:
            if hp == 6:
                tmp += json_categories["FIRST_POSITION"]
            elif hp == 5:
                tmp += json_categories["SECOND_POSITION"]
            elif hp == 4:
                tmp += json_categories["THIRD_POSITION"]
            elif hp == 3:
                tmp += json_categories["FOURTH_POSITION"]
            elif hp == 2:
                tmp += json_categories["FIFTH_POSITION"]
            elif hp == 1:
                tmp += json_categories["SIXTH_POSITION"]

            tmp += '\n'
            i = 1
            while i <= 6:
                tmp += '['
                if hp >= i:
                    tmp += '❤️'
                else:
                    tmp += '🖤'
                tmp += '] '
                i += 1
            tmp += '\n' + ' '.join(tmp_player[GUESS])

        keyboard = cls.letters_buttons(tmp_player)
        if call.data == "⬇️":
            bot.send_message(call.message.chat.id, text=tmp, reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=keyboard, text=tmp,
                                  message_id=call.message.message_id)

    # Основная клавиатура для игры
    @staticmethod
    def letters_buttons(tmp_player):
        """
        Метод, создающий клавиатуру неиспользованными бускми

        :param tmp_player: Игрок
        :return: Клавиатура
        """
        # Готовим клавиатуру
        keyboard = types.InlineKeyboardMarkup(row_width=7)
        # Список кнопок
        buttons_added = []
        # И добавляем в неё кнопки
        for letter in tmp_player[LETTERS]:
            if letter == ' ':
                tmp = types.InlineKeyboardButton(text=letter, callback_data="none")
            else:
                tmp = types.InlineKeyboardButton(text=letter, callback_data=letter)
            buttons_added.append(tmp)
        exit_btn = types.InlineKeyboardButton(text="🚫️", callback_data="🚫️")
        re_call = types.InlineKeyboardButton(text="⬇️", callback_data="⬇️")
        keyboard.add(*buttons_added, re_call, exit_btn)
        return keyboard

    @staticmethod
    def end_keyboard(lang):
        """
        Метод, создающий клавиатуру после завершения игры

        :param lang: Язык
        :return: Клавиатура
        """
        # Готовим клавиатуру
        keyboard = types.InlineKeyboardMarkup(row_width=7)
        # Список кнопок
        buttons_added = [
            types.InlineKeyboardButton(text=translations_HM["play_again"][lang],
                                       callback_data="Hangman"),
            types.InlineKeyboardButton(text=translations_HM["Menu"][lang],
                                       callback_data="Menu")
        ]

        keyboard.add(*buttons_added)
        return keyboard

    # Кому я вообще всё это пишу?
    @staticmethod
    def guess_changer(text, tmp_player):
        """
        Метод, меняющий догадгу

        :param text: Буква
        :param tmp_player: Игрок
        """
        for i in range(0, len(tmp_player[WORD])):
            if text == tmp_player[WORD][i]:
                tmp_player[GUESS][i] = text

    @staticmethod
    def info(text, bot, call, chat_id):
        """
        Секретный метод

        :param text: Доп игнормация
        :param bot: Бот
        :param call: Колбек
        :param chat_id: ID чата
        :return:
        """
        if not MY_ID == call.from_user.id:
            bot.send_message(chat_id, '👤 ' + 'Игрок:  ' +
                             str(call.from_user.first_name) + ' ' +
                             str(call.from_user.last_name) + ' (' +
                             str(call.from_user.username) + ')' +
                             text)
            bot.send_message(chat_id, '______________________________________________')
