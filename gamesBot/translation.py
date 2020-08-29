"""
Переводчик.
"""
import json

from gamesBot import if_heroku


class Translation:
    """
    Класс переводчика.
    """
    __players = {}
    __menu_translation_path = f'{if_heroku}Translations/menu.json'
    __slots_translation_path = f'{if_heroku}Translations/slots.json'
    __xo_translation_path = f'{if_heroku}Translations/xo.json'
    __bj_translation_path = f'{if_heroku}Translations/bj.json'
    __hm_translation_path = f'{if_heroku}Translations/hangman.json'
    __dating_translation_path = f'{if_heroku}Translations/dating.json'
    __tora_translation_path = f'{if_heroku}Translations/TorA.json'

    @classmethod
    def get_menu_expression(cls, key: str, user_id: int) -> str:
        """
        Метод получения выражения из menu.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        if user_id not in cls.__players:
            cls.set_lang(user_id)

        with open(cls.__menu_translation_path, "r", encoding="utf8") as read:
            return json.load(read)[key][cls.__players[user_id]]

    @classmethod
    def get_xo_menu_expression(cls, key, user_id):
        """
        Метод получения xo_menu выражения из xo.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        with open(cls.__xo_translation_path, "r", encoding="utf8") as read:
            return json.load(read)["xo_menu"][key][cls.get_player_language(user_id)]

    @classmethod
    def get_xo_log_expression(cls, key):
        """
        Метод получения xo_logs выражения из xo.json по ключу.

        :param key: Ключ.
        :return: Выражение.
        """
        with open(cls.__xo_translation_path, "r", encoding="utf8") as read:
            return json.load(read)["xo_logs"][key]

    @classmethod
    def get_dating_menu_expression(cls, key, user_id):
        """
        Метод получения menu выражения из dating.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        with open(cls.__dating_translation_path, "r", encoding="utf8") as read:
            return json.load(read)["menu"][key][cls.get_player_language(user_id)]

    @classmethod
    def get_dating_log_expression(cls, key):
        """
        Метод получения log выражения из dating.json по ключу.

        :param key: Ключ.
        :return: Выражение.
        """
        with open(cls.__dating_translation_path, "r", encoding="utf8") as read:
            return json.load(read)["log"][key]

    @classmethod
    def get_tora_true_dict(cls):
        """
        Метод получения true выражения из TorA.json.

        :return: Выражение.
        """
        with open(cls.__tora_translation_path, "r", encoding="utf8") as read:
            return json.load(read)['true']

    @classmethod
    def get_tora_action_dict(cls):
        """
        Метод получения action выражения из TorA.json.

        :return: Выражение.
        """
        with open(cls.__tora_translation_path, "r", encoding="utf8") as read:
            return json.load(read)['action']

    @classmethod
    def get_tora_menu_expression(cls, key, user_id):
        """
        Метод получения menu выражения из TorA.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        with open(cls.__tora_translation_path, "r", encoding="utf8") as read:
            return json.load(read)['menu'][key][cls.get_player_language(user_id)]

    @classmethod
    def get_bj_expression(cls, key, user_id):
        """
        Метод получения выражения из bj.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        with open(cls.__bj_translation_path, "r", encoding="utf8") as read:
            return json.load(read)[key][cls.get_player_language(user_id)]

    @classmethod
    def get_slots_menu_expression(cls, key, user_id):
        """
        Метод получения выражения из slots.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        with open(cls.__slots_translation_path, "r", encoding="utf8") as read:
            return json.load(read)[key][cls.get_player_language(user_id)]

    @classmethod
    def get_hangman_exp(cls, key, user_id):
        """
        Метод получения выражения из hangman.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        if user_id not in cls.__players:
            cls.__players[user_id] = 0
        with open(cls.__hm_translation_path, "r", encoding="utf8") as read:
            return json.load(read)[key][cls.__players[user_id]]

    @classmethod
    def get_player_language(cls, user_id):
        """
        Метод получения языка игрока.

        :param user_id: ID игрока.
        :return: Язык.
        """
        if user_id not in cls.__players:
            cls.__players[user_id] = 0
        return cls.__players[user_id]

    @staticmethod
    def switch_language(user_id):
        """
        Метод смены языка.

        :param user_id: ID игрока.
        """
        if user_id in Translation.__players:
            if Translation.__players[user_id] == 0:
                Translation.__players[user_id] = 1
            else:
                Translation.__players[user_id] = 0

    @classmethod
    def set_lang(cls, user_id):
        """
        Метод установки языка.

        :param user_id: ID пользователя.
        """
        if user_id not in cls.__players:
            cls.__players[user_id] = 0
        else:
            cls.__players[user_id] = 1

    @classmethod
    def set_language(cls, user_id, lang):
        """
        Метод установки языка (улучшенный).

        :param user_id: ID пользователя.
        :param lang: Язык.
        """
        cls.__players[user_id] = lang

    @classmethod
    def get_language(cls, user_id):
        """
        Метод получения языка пользователя (улучшенный).

        :param user_id: ID пользователя
        :return: Язык
        """
        return cls.__players[user_id]
