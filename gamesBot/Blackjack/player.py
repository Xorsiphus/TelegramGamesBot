"""
Игрок.
"""
from . import Deck
from . import Card


class Player:
    """
    Класс игрока.
    """
    card_points = {"Ace": (1, 11),
                   "2": 2,
                   "3": 3,
                   "4": 4,
                   "5": 5,
                   "6": 6,
                   "7": 7,
                   "8": 8,
                   "9": 9,
                   "10": 10,
                   "Jack": 10,
                   "Queen": 10,
                   "King": 10
                   }

    def __init__(self, name, telegram_id, balance):
        """
        Инициализирует новый экземпляр класса игрок.

        :param name: Имя игрока.
        :param telegram_id: ID игрока в Телеграме.
        :param balance: Баланс.
        """
        self.__name = name
        self.__telegram_id = telegram_id
        self.__balance = balance
        self.__deck = Deck()
        self.__player_cards = []
        self.__player_points = 0
        self.__dealer_cards = []
        self.__dealer_points = 0
        self.__is_first_round = True
        self.__is_player_active = True
        self.__is_dealer_active = True
        self.__stop_the_game = False
        self.__winner = None

    @property
    def deck(self):
        """
        Геттер колоды карт.

        :return: Колода.
        """
        return self.__deck

    @property
    def player_cards(self):
        """
        Геттер карт игрока.

        :return: Карты игрока.
        """
        return self.__player_cards

    @property
    def dealer_cards(self):
        """
        Геттер карт дилера.

        :return: Карты дилера.
        """
        return self.__dealer_cards

    @property
    def is_player_active(self):
        """
        Геттер значения активен ли игрок.

        :return: Значение активен ли игрок.
        """
        return self.__is_dealer_active

    @is_player_active.setter
    def is_player_active(self, is_player_active):
        """
        Сеттер значения активен ли игрок.

        :param is_player_active: Значение активен ли игрок.
        """
        if type(is_player_active) == bool:
            self.__is_player_active = is_player_active

    @property
    def stop_the_game(self):
        """
        Геттер значения закончилась ли игра.

        :return: Значение закончилась ли игра.
        """
        return self.__stop_the_game

    @property
    def name(self):
        """
        Геттер имени игрока.

        :return: Имя игрока.
        """
        return self.__name

    @property
    def telegram_id(self):
        """
        Геттер ID Телеграма игрока.

        :return: ID Телеграма игрока.
        """
        return self.__telegram_id

    @property
    def balance(self):
        """
        Геттер баланса.

        :return: Значение баланса.
        """
        return self.__balance

    def next_round(self):
        """
        Метод, отвечающий за любой раунд игр Блекджек после первого.
        """
        if self.__is_dealer_active is False and self.__is_player_active is False:
            self.__stop_the_game = True
        else:
            game_condition = self.__game_condition()

            options = {"first": self.__first_round,
                       "both": self.__round_both,
                       "player": self.__round_player,
                       "dealer": self.__round_dealer}

            options[game_condition]()

            if self.__player_points >= 21 or self.__dealer_points >= 21:
                self.__stop_the_game = True

            if self.__stop_the_game and self.__is_first_round:
                self.__is_first_round = True
            else:
                self.__is_first_round = False

            if self.__dealer_points >= 17:
                self.__is_dealer_active = False

            if self.__is_dealer_active is False and self.__is_player_active is False:
                self.__stop_the_game = True

    def __game_condition(self):
        """
        Метод, возвращающий состояние игры в виде строки.

        :return: Состояние игры.
        """
        if self.__is_first_round:
            return "first"
        if self.__is_player_active and self.__is_dealer_active:
            return "both"
        elif self.__is_player_active:
            return "player"
        elif self.__is_dealer_active:
            return "dealer"

    def __first_round(self):
        """
        Метод, отвечающий за первый раунд игры Блекджек.
        """
        player_first_card = self.__deck.pop_card_from_deck()
        player_second_card = self.__deck.pop_card_from_deck()
        self.__player_cards.extend([player_first_card, player_second_card])

        dealer_first_card = self.__deck.pop_card_from_deck()
        dealer_second_card = self.__deck.pop_card_from_deck()
        self.__dealer_cards.extend([dealer_first_card, dealer_second_card])

        self.__player_points = Player.calculate_points_two_cards_first_round(player_first_card, player_second_card)
        self.__dealer_points = Player.calculate_points_two_cards_first_round(dealer_first_card, dealer_second_card)

    def __round_both(self):
        """
        Метод, комбинирующий методы round_player() и round_dealer().
        """
        self.__round_player()
        self.__round_dealer()

    def __round_player(self):
        """
        Метод, отвечающий за раунд игрока.
        """
        player_card = self.__deck.pop_card_from_deck()
        self.__player_cards.append(player_card)

        self.__player_points = Player.recalculate_points(self.__player_cards)

    def __round_dealer(self):
        """
        Метод, отвечающий за раунд дилера.
        """
        dealer_card = self.__deck.pop_card_from_deck()
        self.__dealer_cards.append(dealer_card)

        self.__dealer_points = Player.recalculate_points(self.__dealer_cards)

    def __define_winner(self):
        """
        Метод, определяющий победителя в конце игры.
        """
        if self.__player_points > 21 or self.__dealer_points > 21:
            if self.__player_points < 21:
                self.__winner = "Player"
            else:
                self.__winner = "Dealer"
        else:
            if self.__player_points == self.__dealer_points:
                self.__winner = "Push"
            elif self.__player_points < self.__dealer_points:
                self.__winner = "Dealer"
            else:
                self.__winner = "Player"

    def lose_the_game(self):
        """
        Метод, отменяющий остановку игры.
        """
        self.__stop_the_game = False

    @staticmethod
    def display_all_cards(cards: []):
        """
        Метод, выводящий информацию обо всех предоставленных картах.

        :param cards: Предоставленные карты.
        :return: Информация о картах
        """
        message = ""

        for card in cards:
            card_info = card.display_card_info()
            message += f"[{card_info}], "

        return message

    @staticmethod
    def recalculate_points(cards: []):
        """
        Метод, рассчитывающий число очков на основании предоставленных карт.

        :param cards: Предоставленные карты.
        :return: Рассчитанное число очков.
        """
        points = 0

        ace_cards = []

        for card in cards:
            if card.value == "Ace":
                ace_cards.append(card)
            else:
                points += Player.card_points[card.value]

        for ace_card in ace_cards:
            if points > 10:
                points += Player.card_points[ace_card.value][0]
            else:
                points += Player.card_points[ace_card.value][1]

        return points

    @staticmethod
    def calculate_points_two_cards_first_round(first_card: Card, second_card: Card):
        """
        Метод, рассчитывающий число очков в первом раунде.

        :param first_card: Первая карта.
        :param second_card: Вторая карта.
        :return: Рассчитанное число очков.
        """
        if first_card.value != "Ace" and second_card.value != "Ace":
            points = Player.card_points[first_card.value] + Player.card_points[second_card.value]
        elif first_card.value == "Ace" and second_card.value != "Ace":
            points = Player.card_points["Ace"][1] + Player.card_points[second_card.value]
        elif first_card.value != "Ace" and second_card.value == "Ace":
            points = Player.card_points[first_card.value] + Player.card_points["Ace"][1]
        else:
            points = 11

        return points

    def display_first_round(self, language):
        """
        Метод, выводяищий информацию о первом раунде.

        :param language: Язык.
        :return: Информация о первом раунде.
        """
        result_message = ""

        if language == 0:
            result_message = f"Игра Началась!\n" \
                             f"Карты дилера: [{self.__dealer_cards[0].display_card_info()}], [--]\n\n" \
                             f"Ваши карты: {Player.display_all_cards(self.__player_cards)}\n" \
                             f"Сумма очков: {self.__player_points}\n"
        elif language == 1:
            result_message = f"Game has started!\n" \
                             f"Dealer's cards: [{self.__dealer_cards[0].display_card_info()}], [--]\n\n" \
                             f"Your cards: {Player.display_all_cards(self.__player_cards)}\n" \
                             f"Sum of points: {self.__player_points}\n"

        return result_message

    def display_player_round(self, p_language):
        """
        Метод, выводяищий информацию о раунде игрока.

        :param p_language: Язык.
        :return: Информация о раунде игрока.
        """
        result_message = ""

        if p_language == 0:
            result_message = f"Вы взяли карту: [{self.__player_cards[-1].display_card_info()}]\n" \
                             f"Ваши карты: {Player.display_all_cards(self.__player_cards)}\n" \
                             f"Сумма очков: {self.__player_points}\n"
        elif p_language == 1:
            result_message = f"You take a card: [{self.__player_cards[-1].display_card_info()}]\n" \
                             f"Your cards: {Player.display_all_cards(self.__player_cards)}\n" \
                             f"Sum of points: {self.__player_points}\n"

        return result_message

    def display_result(self, language):
        """
        Метод, выводяищий информацию о результате игры.

        :param language: Язык.
        :return: Информация о результате игры.
        """
        self.__define_winner()
        result_message = ""

        if language == 0:
            winner_options = {"Dealer": "Дилер выиграл",
                              "Player": "Вы выиграли",
                              "Push": "Ничья"}

            if self.__is_first_round:
                result_message = f"Игра началась!\n"
            result_message += f"Игра завершилась!\n" \
                              f"Карты дилера: {Player.display_all_cards(self.__dealer_cards)}\n" \
                              f"Сумма очков: {self.__dealer_points}\n\n" \
                              f"Ваши карты: {Player.display_all_cards(self.__player_cards)}\n" \
                              f"Сумма очков: {self.__player_points}\n\n" \
                              f"Результат: {winner_options[self.__winner]}"
        elif language == 1:
            winner_options = {"Dealer": "Dealer won",
                              "Player": "You won",
                              "Push": "Push"}

            if self.__is_first_round:
                result_message = f"Game has started!\n"
            result_message += f"Game has finished!\n" \
                              f"Dealer's cards: {Player.display_all_cards(self.__dealer_cards)}\n" \
                              f"Sum of points: {self.__dealer_points}\n\n" \
                              f"Your cards: {Player.display_all_cards(self.__player_cards)}\n" \
                              f"Sum of points: {self.__player_points}\n\n" \
                              f"Result: {winner_options[self.__winner]}"

        return result_message
