# Класс игрока


class Player:
    def __init__(self, name, telegram_id, balance):
        self.__name = name
        self.__telegram_id = telegram_id
        self.__balance = balance

    @property
    def name(self):
        return self.__name

    @property
    def telegram_id(self):
        return self.__telegram_id

    @property
    def balance(self):
        return self.__balance
