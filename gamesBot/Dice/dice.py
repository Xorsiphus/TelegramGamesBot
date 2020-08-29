"""
Кости.
"""
import random
from gamesBot import Translation


class Dice:
    """
    Класс игры в кости.
    """
    dice = [1, 2, 3, 4, 5, 6]

    @classmethod
    def get_dice(cls, user_id, message, chat_type):
        """
        Метод бросания костей.

        :param user_id: ID пользователя.
        :param message: Полученное сообщение.
        :param chat_type: Тип чата.
        :return:
        """

        if chat_type[7:] == "Dice":
            print(message.json)
            before = message.json["reply_markup"]["inline_keyboard"][2][1]['text']
            text = str(random.choice(cls.dice)) + '️⃣' + str(random.choice(cls.dice)) + '️⃣'
            if before == text:
                text = cls.get_dice(user_id, message, chat_type)
            return text
        else:
            return Translation.get_menu_expression(key="Dice", user_id=user_id)
