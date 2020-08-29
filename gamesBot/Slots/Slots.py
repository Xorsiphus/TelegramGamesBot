"""
Слоты.
"""
from gamesBot import Translation
import random
from telebot import types


class Slots:
    """
    Класс игры Слоты.
    """
    @property
    def flag(self):
        """
        Геттер флага.

        :return: Флаг.
        """
        return self.__flag

    # Поток обработки сообщений
    @staticmethod
    def main_slots(call, bot):
        """
        Метод редактирования сообщения и кнопки при колбеке "Slots".

        :param call: Колбек.
        :param bot: Бот.
        """
        markup = types.InlineKeyboardMarkup(row_width=3)
        b = types.InlineKeyboardButton(Translation.get_slots_menu_expression("spin", call.from_user.id),
                                       callback_data='spin')
        markup.add(b)
        bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=markup,
                              text=Translation.get_slots_menu_expression("slots", call.from_user.id),
                              message_id=call.message.message_id)

    @classmethod
    def callback_inline(cls, call, bot):
        """
        Метод обработки колбеков.

        :param call: Колбек.
        :param bot: Бот.
        """
        cls.__flag = True

        if call.data == "Slots":
            cls.main_slots(call, bot)
            return

        # Код при нажатии на "Play Slots" в меню (сама игра "Слот-Машина")
        if call.data == 'spin':
            i = 0
            array = []

            # Генерация случайного списка, от которого зависит выигрыш
            while i < 9:
                array.append(random.randint(0, 4))
                i = i + 1
            new_array = []
            i = 0

            # Замена случайных чисел на картинки для наглядности
            while i < 9:
                if array[i] == 0:
                    new_array.append("7️⃣")
                elif array[i] == 1:
                    new_array.append("🍒")
                elif array[i] == 2:
                    new_array.append("🍋")
                elif array[i] == 3:
                    new_array.append("🍎")
                elif array[i] == 4:
                    new_array.append("🍉")
                i += 1

            # Удаление inline-кнопки у предыдущего сообщения (остаётся только сообщение "Slots: ")
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=None, text=call.message.text,
                                  message_id=call.message.message_id)

            # Подготовка inline-кнопок "Spin!" и "Exit" к следующему сообщению
            markup = types.InlineKeyboardMarkup(row_width=3)
            b1 = types.InlineKeyboardButton(Translation.get_slots_menu_expression("spin", call.from_user.id),
                                            callback_data='spin')
            b2 = types.InlineKeyboardButton(Translation.get_slots_menu_expression("exit", call.from_user.id),
                                            callback_data='Menu')
            markup.add(b1, b2)

            # Крепление inline-меню (кнопки "Spin!" и "Exit") и вывод слотов пользователю
            message_string = Translation.get_slots_menu_expression("output", call.from_user.id)
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=markup,
                                  text="{}\n{}{}{}\n{}{}{}\n{}{}{}".format(message_string, *new_array),
                                  message_id=call.message.message_id)

            # Проверка выигрыша (на данный момент просто проверка всех строк и столбцов)
            # При удовлетворении условию выводится уведомление с поздравлением
            if new_array[0] == new_array[1] == new_array[2] or new_array[3] == new_array[4] == new_array[5] or \
                    new_array[6] == new_array[7] == new_array[8] or new_array[0] == new_array[3] == new_array[6] or \
                    new_array[1] == new_array[4] == new_array[7] or new_array[2] == new_array[5] == new_array[8]:
                bot.answer_callback_query(callback_query_id=call.id, text="Jackpot!!!", show_alert=True)
