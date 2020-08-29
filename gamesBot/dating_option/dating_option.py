"""
Функция поиска собеседника.
"""
from gamesBot import Translation
from gamesBot import if_heroku

from telebot import types

import random


class Dating_class:
    """
    Класс поисковика.
    """
    call_list = ["Dating_start", "Dating_fill", "Dating_find", 'Dating_stop', "Dating_show_profile", "Dating_skip",
                 "get_link"]

    __players = {}
    __player_questionnaire_filling_status = {}
    __player_counter = {}
    __last_bot_message = {}
    __current_buddy = {}

    @classmethod
    def dating_lobby_handler(cls, call, bot, menu_keyboard):
        """
        Метод, обрабатывающий колбеки.

        :param call: Колбек.
        :param bot: Бот.
        :param menu_keyboard: Разметка прикрепляемой клавиатуры-меню.
        """
        if call.data == "Dating_start":
            if cls.__players.get(call.from_user.id, -1) == -1:
                cls.init_player(call.from_user.id)
                cls.__players[call.from_user.id]['username'] = call.from_user.username
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  reply_markup=cls.gen_dating_markup(call.message.chat.id),
                                  text=Translation.get_dating_menu_expression("dating_menu", user_id=call.from_user.id),
                                  message_id=call.message.message_id)

        elif call.data == 'get_link':
            try:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      reply_markup=cls.gen_finder_markup(call.message.chat.id),
                                      text='@' + str(
                                          cls.__players[cls.__current_buddy[call.message.chat.id]]['username']),
                                      message_id=call.message.message_id)
            except Exception as err:
                print(Translation.get_dating_log_expression("msg edit error").format(err))

        elif call.data == "Dating_fill" and Dating_class.check_id_in_lobby_dict(call.from_user.id,
                                                                                call.message.chat.type):
            if call.from_user.username is None:
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          text=Translation.get_dating_menu_expression("none_error",
                                                                                      user_id=call.from_user.id),
                                          reply_markup=cls.gen_dating_markup(call.from_user.id),
                                          message_id=call.message.message_id)
                except Exception as err:
                    print(Translation.get_dating_log_expression("msg edit error").format(err))
                return

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  text=Translation.get_dating_menu_expression("fill_name",
                                                                              user_id=call.from_user.id),
                                  reply_markup=cls.gen_skip_markup(call.message.chat.id),
                                  message_id=call.message.message_id)
            cls.set_last_bot_message(call.from_user.id, call.message.message_id)
            cls.__player_questionnaire_filling_status[call.from_user.id] = {"status": 1}

        elif call.data == "Dating_find":
            bot.edit_message_text(chat_id=call.from_user.id,
                                  text=Translation.get_dating_menu_expression("fill_out",
                                                                              user_id=call.from_user.id),
                                  message_id=call.message.message_id)
            Dating_class.player_finder(call, bot)

        elif call.data == "Dating_skip" and Dating_class.check_id_in_lobby_dict(call.from_user.id,
                                                                                call.message.chat.type):
            if cls.__player_questionnaire_filling_status[call.from_user.id]['status'] < 4:
                cls.send_next_step(bot, call.from_user.id)
            else:
                cls.set_profile_flag(call.from_user.id)
                call.data = 'Dating_show_profile'
                cls.dating_lobby_handler(call, bot, menu_keyboard)
                return
            Dating_class.next_filler_step(call.from_user.id)

        elif call.data == "Dating_stop" and Dating_class.check_id_in_lobby_dict(call.from_user.id,
                                                                                call.message.chat.type):
            Dating_class.stopper(call, bot, menu_keyboard)

        elif call.data == "Dating_show_profile":
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  text=Translation.get_dating_menu_expression("profile_info",
                                                                              user_id=call.from_user.id),
                                  message_id=call.message.message_id)
            Dating_class.show_player_profile(bot, call.message.chat.id, call.message.chat.type, True)

        if call.data == "Dating_start":
            print(cls.__players)

    @classmethod
    def init_player(cls, user_id):
        """
        Метод, инициализирующий игрока.

        :param user_id: ID пользователя.
        """
        cls.__player_questionnaire_filling_status[user_id] = {"status": 1}
        cls.__player_counter[user_id] = user_id
        cls.__players[user_id] = cls.init_default_player_info()

    @classmethod
    def set_last_bot_message(cls, user_id, message_id):
        """
        Метод, запоминающий ID последнего сообщения от бота для каждого пользователя.

        :param user_id: ID пользователя.
        :param message_id: ID сообщения.
        """
        cls.__last_bot_message[user_id] = message_id

    @classmethod
    def dating_message_handler(cls, bot, message):
        """
        Метод, обрабатывающий ввод пользователя, при заполнении анкеты.

        :param bot: Бот.
        :param message: Сообщение.
        """
        if Dating_class.check_filling_status(message.from_user.id) in [1, 2, 3, 4]:
            if message.content_type == "photo" and Dating_class.check_filling_status(
                    message.from_user.id) == 4:
                image_info = bot.get_file(message.photo[-1].file_id)
                image = bot.download_file(image_info.file_path)
                src = f"{if_heroku}dating_option/images/{str(message.from_user.id)}.jpg"
                with open(src, 'wb') as new_file:
                    new_file.write(image)
                Dating_class.questionnaire_filler(bot, message, src)
            Dating_class.questionnaire_filler(bot, message, message.text)
            return

    @classmethod
    def send_next_step(cls, bot, user_id):
        """
        Метод, отправющий следующую инструкцию по заполнению анкеты.

        :param bot: Бот.
        :param user_id: ID пользователя.
        """
        if cls.__player_questionnaire_filling_status[user_id]['status'] == 1:
            bot.edit_message_text(chat_id=user_id,
                                  text=Translation.get_dating_menu_expression("fill_name",
                                                                              user_id=user_id),
                                  reply_markup=None,
                                  message_id=cls.__last_bot_message[user_id])
            cls.__last_bot_message[user_id] = bot.send_message(user_id,
                                                               Translation.get_dating_menu_expression("fill_age",
                                                                                                      user_id),
                                                               reply_markup=cls.gen_skip_markup(user_id)).message_id
        if cls.__player_questionnaire_filling_status[user_id]['status'] == 2:
            bot.edit_message_text(chat_id=user_id,
                                  text=Translation.get_dating_menu_expression("fill_age",
                                                                              user_id=user_id),
                                  reply_markup=None,
                                  message_id=cls.__last_bot_message[user_id])
            cls.__last_bot_message[user_id] = bot.send_message(user_id,
                                                               Translation.get_dating_menu_expression("fill_city",
                                                                                                      user_id),
                                                               reply_markup=cls.gen_skip_markup(user_id)).message_id
        if cls.__player_questionnaire_filling_status[user_id]['status'] == 3:
            bot.edit_message_text(chat_id=user_id,
                                  text=Translation.get_dating_menu_expression("fill_city",
                                                                              user_id=user_id),
                                  reply_markup=None,
                                  message_id=cls.__last_bot_message[user_id])
            cls.__last_bot_message[user_id] = bot.send_message(user_id,
                                                               Translation.get_dating_menu_expression("get_photo",
                                                                                                      user_id),
                                                               reply_markup=cls.gen_skip_markup(user_id)).message_id

    @classmethod
    def get_needed_phrase(cls, user_id):
        """
        Метод, достающий нужную фразу, в зависимоти от стадии заполнения анкеты.

        :param user_id: ID пользователя.
        :return: Нужная фраза, зависит от стадии заполнения анкеты.
        """
        if cls.__player_questionnaire_filling_status[user_id]['status'] == 1:
            return Translation.get_dating_menu_expression("fill_name", user_id)
        elif cls.__player_questionnaire_filling_status[user_id]['status'] == 2:
            return Translation.get_dating_menu_expression("fill_age", user_id)
        elif cls.__player_questionnaire_filling_status[user_id]['status'] == 3:
            return Translation.get_dating_menu_expression("fill_city", user_id)
        elif cls.__player_questionnaire_filling_status[user_id]['status'] == 4:
            return Translation.get_dating_menu_expression("get_photo", user_id)

    @classmethod
    def questionnaire_filler(cls, bot, message, message_text):
        """
        Метод, обрабатывающий полученные данные от пользователя и заполняющий анкету.

        :param bot: Бот.
        :param message: Сообщение.
        :param message_text: Сообщение.
        """
        user_id = message.from_user.id
        if cls.__player_questionnaire_filling_status[user_id]['status'] == 1:
            if message_text != "":
                cls.__players[user_id]["name"] = message_text
            cls.send_next_step(bot, user_id)
            cls.next_filler_step(user_id)
            return
        ###########################
        if cls.__player_questionnaire_filling_status[user_id]['status'] == 2 and message_text.isdigit():
            if message_text != "":
                cls.__players[user_id]["age"] = message_text
            cls.send_next_step(bot, user_id)
            cls.next_filler_step(user_id)
            return

        if cls.__player_questionnaire_filling_status[user_id]['status'] == 2:
            bot.edit_message_text(chat_id=user_id,
                                  text=Translation.get_dating_menu_expression("fill_age",
                                                                              user_id=user_id),
                                  reply_markup=None,
                                  message_id=cls.__last_bot_message[user_id])
            cls.__last_bot_message[user_id] = bot.send_message(user_id,
                                                               Translation.get_dating_menu_expression("fill_age",
                                                                                                      user_id),
                                                               reply_markup=cls.gen_skip_markup(user_id)).message_id
            return
        ###########################
        if cls.__player_questionnaire_filling_status[user_id]['status'] == 3:
            if message_text != "":
                cls.__players[user_id]["city"] = message_text
            cls.send_next_step(bot, user_id)
            cls.next_filler_step(user_id)
            return
        ###########################
        if cls.__player_questionnaire_filling_status[user_id]['status'] == 4 and message.content_type == 'photo':
            if message_text != "":
                cls.__players[user_id]["image"] = message_text
            ###########################
            cls.__player_questionnaire_filling_status[user_id]["status"] = 0
            cls.set_profile_flag(user_id)

            bot.edit_message_text(chat_id=user_id,
                                  text=Translation.get_dating_menu_expression("get_photo",
                                                                              user_id=user_id),
                                  reply_markup=None,
                                  message_id=cls.__last_bot_message[user_id])

            if user_id not in cls.__player_counter:
                cls.__player_counter[user_id] = user_id
            cls.show_player_profile(bot, user_id, message.chat.type, True)

    @classmethod
    def set_profile_flag(cls, user_id):
        """
        Метод, помечающий профиль как заполненный.

        :param user_id: ID пользователя.
        """
        cls.__players[user_id]['fill_out_flag'] = True

    @classmethod
    def gen_player_profile(cls, user_id):
        """
        Метод, генерирующий профиль игрока.

        :param user_id: ID пользователя.
        :return: Профиль игрока.
        """
        description = Translation.get_dating_menu_expression("name", user_id) + ": " + str(
            cls.__players[user_id]["name"]) + "\n"
        description += Translation.get_dating_menu_expression("age", user_id) + ": " + str(
            cls.__players[user_id]["age"]) + "\n"
        description += Translation.get_dating_menu_expression("city", user_id) + ": " + str(
            cls.__players[user_id]["city"])

        image = open(cls.__players[user_id]["image"], "rb")
        return {"description": description, "image": image}

    @classmethod
    def show_player_profile(cls, bot, user_id, chat_type, flag):
        """
        Метод, выводящий профиль пользователя.

        :param bot: Бот.
        :param user_id: ID пользователя.
        :param chat_type: Тип чата.
        :param flag: Пометка.
        """
        if cls.check_id_profile(user_id, chat_type):

            profile = cls.gen_player_profile(user_id)

            bot.send_photo(user_id, profile['image'], profile['description'])

            markup = types.InlineKeyboardMarkup()
            if flag:
                markup.add(
                    types.InlineKeyboardButton(Translation.get_dating_menu_expression("again", user_id),
                                               callback_data='Dating_fill'))
            markup.add(
                types.InlineKeyboardButton(Translation.get_dating_menu_expression("end_filling", user_id),
                                           callback_data='Dating_start'))
            bot.send_message(user_id, Translation.get_dating_menu_expression("submenu", user_id),
                             reply_markup=markup)
        else:
            bot.send_message(user_id, text=Translation.get_dating_menu_expression("profile_error",
                                                                                  user_id=user_id),
                             reply_markup=cls.gen_dating_markup(user_id))

    @classmethod
    def player_finder(cls, call, bot):
        """
        Метод, отвечающий за непосредственный поиск собеседника.

        :param call: Колбек.
        :param bot: Бот.
        """

        if call.message.chat.id not in cls.__player_counter:
            cls.__player_counter[call.message.chat.id] = call.message.chat.id

        if Dating_class.check_id_profile(call.message.chat.id, call.message.chat.type):
            if len(cls.__players) == 1:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      reply_markup=cls.gen_dating_markup(call.message.chat.id),
                                      text=Translation.get_dating_menu_expression("buddy_error", call.from_user.id),
                                      message_id=call.message.message_id)
                return

            buddy_id = cls.get_unique_player_id(call.message.chat.id)
            cls.__player_counter[call.message.chat.id] = buddy_id
            cls.__current_buddy[call.message.chat.id] = buddy_id

            profile = cls.gen_player_profile(buddy_id)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  text=Translation.get_dating_menu_expression("buddy", user_id=call.message.chat.id),
                                  message_id=call.message.message_id)
            bot.send_photo(call.message.chat.id, profile['image'], profile['description'])
            bot.send_message(call.message.chat.id,
                             Translation.get_dating_menu_expression("dating_menu", user_id=call.message.chat.id),
                             reply_markup=cls.gen_finder_markup(call.message.chat.id))
            return

        else:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  reply_markup=cls.gen_dating_markup(call.message.chat.id),
                                  text=Translation.get_dating_menu_expression("profile_error", call.message.chat.id),
                                  message_id=call.message.message_id)

    @classmethod
    def get_unique_player_id(cls, user_id):
        """
        Метод, получающий нового игрока для отображения в поиске.

        :param user_id: ID пользователя.
        :return: ID нового игрока для отображения.
        """
        result_id = user_id
        if len(cls.__players) == 2:
            cls.__player_counter[user_id] = user_id
        while result_id == cls.__player_counter[user_id] or result_id == user_id:
            result_id = random.choice(list(cls.__players.keys()))
        return result_id

    @classmethod
    def next_filler_step(cls, user_id):
        """
        Метод, меняющий стадию заполнения анкеты.

        :param user_id: ID пользователя.
        """
        cls.__player_questionnaire_filling_status[user_id]['status'] += 1

    @classmethod
    def check_id_in_lobby_dict(cls, user_id, chat_type):
        """
        Метод, проверяющий игрока на наличие в словаре игроков(созданный профиль).

        :param user_id: ID пользователя.
        :param chat_type: Тип чата.
        :return: Логическое выражение(Существование профиля игрока).
        """
        if chat_type == "private":
            if user_id in cls.__players:
                return 1
            else:
                return 0

    @classmethod
    def check_id_profile(cls, user_id, chat_type):
        """
        Метод, проверяющий ID пользователя на заполнение.

        :param user_id: ID пользователя.
        :param chat_type: Тип чата.
        :return: Логическое значение(Статус заполнения профиля).
        """
        if chat_type == "private":
            if user_id in cls.__players:
                if cls.__players[user_id]["fill_out_flag"]:
                    return 1
                else:
                    return 0
        else:
            return 0

    @classmethod
    def gen_dating_markup(cls, user_id):
        """
        Метод, генерирующий клавиатуру поисковика.

        :param user_id: ID пользователя.
        :return: Клавиатура-меню поисковика.
        """
        markup = types.InlineKeyboardMarkup(row_width=3)
        b1 = types.InlineKeyboardButton(Translation.get_dating_menu_expression("fill_out", user_id),
                                        callback_data='Dating_fill')
        b2 = types.InlineKeyboardButton(Translation.get_dating_menu_expression("show_profile", user_id),
                                        callback_data='Dating_show_profile')
        b3 = types.InlineKeyboardButton(Translation.get_dating_menu_expression("find_a_buddy", user_id),
                                        callback_data='Dating_find')
        b4 = types.InlineKeyboardButton(Translation.get_dating_menu_expression("Exit", user_id),
                                        callback_data='Dating_stop')
        markup.add(b1)
        markup.add(b2)
        markup.add(b3)
        markup.add(b4)
        return markup

    @classmethod
    def gen_finder_markup(cls, user_id):
        """
        Метод, генерирующий клавиатуру для непосредственного поиска.

        :param user_id: ID пользователя.
        :return: Клавиатура-меню непосредственного поиска.
        """
        markup = types.InlineKeyboardMarkup(row_width=3)
        b1 = types.InlineKeyboardButton(Translation.get_dating_menu_expression("Next_buddy", user_id),
                                        callback_data='Dating_find')
        b2 = types.InlineKeyboardButton(Translation.get_dating_menu_expression("show_buddy_info", user_id),
                                        callback_data='get_link')
        b3 = types.InlineKeyboardButton("Exit", callback_data='Dating_start')

        markup.add(b1)
        markup.add(b2)
        markup.add(b3)
        return markup

    @classmethod
    def check_filling_status(cls, user_id):
        """
        Метод, проверяющий статус заполнения анкеты.

        :param user_id: ID пользователя.
        :return: Значение статуса заполнения профиля.
        """
        if user_id in cls.__players:
            return cls.__player_questionnaire_filling_status[user_id]["status"]
        else:
            return 0

    @classmethod
    def init_default_player_info(cls):
        """
        Метод, создающий профиль игрока по умолчанию.

        :return: Новый профиль, заполненный по умолчанию.
        """
        return {"name": "Иван", "city": "Расия", "age": 9, "image": f"{if_heroku}dating_option/images/default.jpg",
                "fill_out_flag": False, "username": "undefined"}

    @staticmethod
    def gen_skip_markup(user_id):
        """
        Метод, генерирующий клавиатуру для пропуска.

        :return: Клавиатура-меню для пропуска.
        """
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(Translation.get_dating_menu_expression("skip_expr", user_id),
                                              callback_data='Dating_skip'))
        return markup

    @classmethod
    def stopper(cls, call, bot, menu_keyboard):
        """
        Метод, останавливающий функцию поиска.

        :param call: Колбэк.
        :param bot: Бот.
        :param menu_keyboard: Разметка прикрепляемой клавиатуры-меню.
        """
        try:
            bot.edit_message_text(chat_id=call.from_user.id, reply_markup=menu_keyboard,
                                  text=Translation.get_dating_menu_expression("disconnect msg", call.from_user.id),
                                  message_id=call.message.message_id)
        except Exception as err:
            print(Translation.get_dating_log_expression("msg edit error").format(err))

        print(cls.__players)

        if len(cls.__players) == 0:
            cls.__players = {}
