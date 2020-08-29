"""
Тест Flask приложения.
"""
import unittest
import urllib.request
from urllib.error import HTTPError


class FlaskTest(unittest.TestCase):
    """
    Класс тестирования Flask приложения.
    """
    def test_index_content(self):
        """
        Метод через запрос проверяет запустилось ли Flask приложение.
        """
        contents = ""
        try:
            contents = str(urllib.request.urlopen("https://games-bot-for-telegram.herokuapp.com/").read())
        except HTTPError as err:
            print(str(err))
            print("Бот не запустился!")

        self.assertEqual("b'!'", contents)


if __name__ == '__main__':
    unittest.main()
