"""
Клавиатура главного меню.
"""
from telebot import types
from gamesBot import Translation


def gen_menu_keyboard(user_id, chat_type):
    """
    Функция генерации клавиатуры главного меню.

    :param user_id: ID пользователя.
    :param chat_type: Тип чата.
    :return: Клавиатура.
    """
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    menu_buttons = [
        types.InlineKeyboardButton(text=Translation.get_menu_expression(key="Blackjack", user_id=user_id),
                                   callback_data="Blackjack"),
        types.InlineKeyboardButton(text=Translation.get_menu_expression(key="Hangman", user_id=user_id),
                                   callback_data="Hangman"),
        types.InlineKeyboardButton(text=Translation.get_menu_expression(key="Slots", user_id=user_id),
                                   callback_data="Slots"),
        types.InlineKeyboardButton(text=Translation.get_menu_expression(key="TorA", user_id=user_id),
                                   callback_data="TorA_start")
    ]
    if chat_type[0:7] == "private":
        menu_buttons.extend([
            types.InlineKeyboardButton(text=Translation.get_menu_expression(key="XO_private", user_id=user_id),
                                       callback_data="XO_start"), types.InlineKeyboardButton(
                text=Translation.get_menu_expression(key="dating", user_id=user_id),
                callback_data="Dating_start")])
    else:
        menu_buttons.append(
            types.InlineKeyboardButton(text=Translation.get_menu_expression(key="XO_private", user_id=user_id),
                                       callback_data="XO_group"))

    menu_buttons.append(
        types.InlineKeyboardButton(text=Translation.get_menu_expression(key="language", user_id=user_id),
                                   callback_data="language"))

    keyboard.add(*menu_buttons)
    return keyboard
