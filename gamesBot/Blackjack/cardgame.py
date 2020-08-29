"""
Карта и колода карт.
"""
from random import shuffle


class Card:
    """
    Класс игральной карты.
    """

    card_values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    card_suits = ["♥", "♦", "♣", "♠"]

    def __init__(self, value, suit):
        """
        Инициализирует новый экземпляр класса карты.

        :param value: Значение карты.
        :param suit: Масть карт.
        """
        self.__value = value
        self.__suit = suit

    @property
    def value(self):
        """
        Геттер значения карты.

        :return: Значение карты.
        """
        return self.__value

    @property
    def suit(self):
        """
        Геттер масти карты.

        :return: Масть карты.
        """
        return self.__suit

    def display_card_info(self):
        """
        Метод вывода информации о карте.

        :return: Строка со мастью и значением карты.
        """
        return f"{self.suit}{self.value}"

    def __str__(self):
        """
        Строковое представление карты.

        :return: Строка со мастью и значением карты.
        """
        return f"{self.suit}{self.value}"


class Deck:
    """
    Класс колоды карт.
    """

    @staticmethod
    def create_deck():
        """
        Метод создания колоды.

        :return: Созданная колода.
        """
        deck = [Card(value, suit) for value in Card.card_values for suit in Card.card_suits]
        return deck

    def __init__(self):
        """
        Инициализирует новый экземпляр класса колоды.
        """
        self.__deck = self.create_deck()

    @property
    def deck(self):
        """
        Геттер колоды.

        :return: Колода.
        """
        return self.__deck

    def shuffle_deck(self):
        """
        Метод перемешивания колоды.
        """
        shuffle(self.deck)

    def pop_card_from_deck(self):
        """
        Метод взятия карты из колоды.

        :return: Карта.
        """
        return self.deck.pop(0)

    def double_deck(self):
        """
        Метод удвоения колоды.
        """
        self.__deck = [Card(value, suit) for value in Card.card_values for suit in Card.card_suits] * 2
