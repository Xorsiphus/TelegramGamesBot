# Класс переводчика


class Translation:
    languages = {"rus": 0, "eng": 1}

    casino_expressions = {"Profile": ("Профиль", "Profile"),
                          "Hello": ("Привет", "Hi"),
                          "Help": ("Напиши /help, чтобы посмотреть мои команды", "Type /help to view my commands"),
                          "Commands": ("Список моих команд:\n 1. /menu - Главное меню игры блекджек\n",
                                       "List of my commands:\n 1. /menu - Main menu of blackjack game"),
                          "Blackjack": ("Блэкджек", "Blackjack"),
                          "Language": ("Сменить язык", "Switch language"),
                          "ChangeLang": ("Язык был сменен", "The language was changed"),
                          "Exit": ("Выйти", "Exit"),
                          "Play": ("Играть", "Play"),
                          "Menu": ("Главное меню", "Main menu"),
                          "Choose": ("Выберите: ", "Choose: "),
                          "ExitFromGame": ("Выходим из игры", "Exiting from the game"),
                          "TakeCard": ("Взять ещё карту", "Take card"),
                          "DoNotTakeCard": ("Больше не брать", "Don't take cards anymore"),
                          "LeaveGame": ("Покинуть игру", "Leave the game"),
                          "LeftGame": ("Покидаем игру", "Left the game"),
                          "ReturnToMenu": ("Возвращаемся  на главное меню", "Going back to the main menu"),
                          "GameIsOver": ("Игра окончена, чтобы начать новую напишите /menu", "Game is over, to start "
                                                                                             "a new game type /menu")
                          }

    def __init__(self, language):
        self.__language = self.languages[language]

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, language):
        if language in ["rus", "eng"]:
            self.__language = self.languages[language]

    def get_casino_expression(self, key):
        return self.casino_expressions[key][self.__language]
