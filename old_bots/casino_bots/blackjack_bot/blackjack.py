# Класс игры блэкджек
from cardgame import Card
from cardgame import Deck
from player import Player


class Blackjack:
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

    def __init__(self, player: Player):
        self.__player = player
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
    def player(self):
        return self.__player

    @property
    def deck(self):
        return self.__deck

    @property
    def player_cards(self):
        return self.__player_cards

    @property
    def dealer_cards(self):
        return self.__dealer_cards

    @property
    def is_player_active(self):
        return self.__is_dealer_active

    @is_player_active.setter
    def is_player_active(self, is_player_active):
        if type(is_player_active) == bool:
            self.__is_player_active = is_player_active

    @property
    def stop_the_game(self):
        return self.__stop_the_game

    @property
    def winner(self):
        return self.__winner

    def lose_the_game(self):
        self.__stop_the_game = False

    @staticmethod
    def display_all_cards(cards: []):
        message = ""

        for card in cards:
            card_info = card.display_card_info()
            message += f"[{card_info}], "

        return message

    @staticmethod
    def recalculate_points(cards: []):
        points = 0

        ace_cards = []

        for card in cards:
            if card.value == "Ace":
                ace_cards.append(card)
            else:
                points += Blackjack.card_points[card.value]

        for ace_card in ace_cards:
            if points > 10:
                points += Blackjack.card_points[ace_card.value][0]
            else:
                points += Blackjack.card_points[ace_card.value][1]

        return points

    @staticmethod
    def calculate_points_two_cards_first_round(first_card: Card, second_card: Card):
        points = 0

        if first_card.value != "Ace" and second_card.value != "Ace":
            points = Blackjack.card_points[first_card.value] + Blackjack.card_points[second_card.value]
        elif first_card.value == "Ace" and second_card.value != "Ace":
            points = Blackjack.card_points["Ace"][1] + Blackjack.card_points[second_card.value]
        elif first_card.value != "Ace" and second_card.value == "Ace":
            points = Blackjack.card_points[first_card.value] + Blackjack.card_points["Ace"][1]
        else:
            points = 11

        return points

    def next_round(self):
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
        if self.__is_first_round:
            return "first"
        if self.__is_player_active and self.__is_dealer_active:
            return "both"
        elif self.__is_player_active:
            return "player"
        elif self.__is_dealer_active:
            return "dealer"

    def __first_round(self):
        player_first_card = self.__deck.pop_card_from_deck()
        player_second_card = self.__deck.pop_card_from_deck()
        self.__player_cards.extend([player_first_card, player_second_card])

        dealer_first_card = self.__deck.pop_card_from_deck()
        dealer_second_card = self.__deck.pop_card_from_deck()
        self.__dealer_cards.extend([dealer_first_card, dealer_second_card])

        self.__player_points = Blackjack.calculate_points_two_cards_first_round(player_first_card, player_second_card)
        self.__dealer_points = Blackjack.calculate_points_two_cards_first_round(dealer_first_card, dealer_second_card)

    def __round_both(self):
        self.__round_player()
        self.__round_dealer()

    def __round_player(self):
        player_card = self.__deck.pop_card_from_deck()
        self.__player_cards.append(player_card)

        self.__player_points = Blackjack.recalculate_points(self.__player_cards)

    def __round_dealer(self):
        dealer_card = self.__deck.pop_card_from_deck()
        self.__dealer_cards.append(dealer_card)

        self.__dealer_points = Blackjack.recalculate_points(self.__dealer_cards)

    def __define_winner(self):
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

    def display_first_round(self, language):
        result_message = ""

        if language == 0:
            result_message = f"Игра Началась!\n" \
                             f"Карты дилера: [{self.__dealer_cards[0].display_card_info()}], [--]\n\n" \
                             f"Ваши карты: {Blackjack.display_all_cards(self.__player_cards)}\n" \
                             f"Сумма очков: {self.__player_points}\n"
        elif language == 1:
            result_message = f"Game has started!\n" \
                             f"Dealer's cards: [{self.__dealer_cards[0].display_card_info()}], [--]\n\n" \
                             f"Your cards: {Blackjack.display_all_cards(self.__player_cards)}\n" \
                             f"Sum of points: {self.__player_points}\n"

        return result_message

    def display_player_round(self, language):
        result_message = ""

        if language == 0:
            result_message = f"Вы взяли карту: [{self.__player_cards[-1].display_card_info()}]\n" \
                             f"Ваши карты: {Blackjack.display_all_cards(self.__player_cards)}\n" \
                             f"Сумма очков: {self.__player_points}\n"
        elif language == 1:
            result_message = f"You take a card: [{self.__player_cards[-1].display_card_info()}]\n" \
                             f"Your cards: {Blackjack.display_all_cards(self.__player_cards)}\n" \
                             f"Sum of points: {self.__player_points}\n"

        return result_message

    def display_result(self, language):
        self.__define_winner()
        result_message = ""

        if language == 0:
            winner_options = {"Dealer": "Дилер выиграл",
                              "Player": "Вы выиграли",
                              "Push": "Ничья"}

            if self.__is_first_round:
                result_message = f"Игра началась!\n"
            result_message += f"Игра завершилась!\n" \
                              f"Карты дилера: {Blackjack.display_all_cards(self.__dealer_cards)}\n" \
                              f"Сумма очков: {self.__dealer_points}\n\n" \
                              f"Ваши карты: {Blackjack.display_all_cards(self.__player_cards)}\n" \
                              f"Сумма очков: {self.__player_points}\n\n" \
                              f"Результат: {winner_options[self.__winner]}"
        elif language == 1:
            winner_options = {"Dealer": "Dealer won",
                              "Player": "You won",
                              "Push": "Push"}

            if self.__is_first_round:
                result_message = f"Game has started!\n"
            result_message += f"Game has finished!\n" \
                              f"Dealer's cards: {Blackjack.display_all_cards(self.__dealer_cards)}\n" \
                              f"Sum of points: {self.__dealer_points}\n\n" \
                              f"Your cards: {Blackjack.display_all_cards(self.__player_cards)}\n" \
                              f"Sum of points: {self.__player_points}\n\n" \
                              f"Result: {winner_options[self.__winner]}"

        return result_message
