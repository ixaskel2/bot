from aiogram.types import ReplyKeyboardMarkup
from lists_bot import*

def main_menu():
    main_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    main_menu.add(
        "💼 Профиль",
        "🌇 Выбор города",
        "🚑 Помощь при передозировках",
        "👨‍⚖️ Поддержка"
    )

    return main_menu

def city_but():
    city_but = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for city in city_list:
        city_but.add(
            city
        )
    city_but.add(
        "📂 Главное меню"
    )
    return city_but


def staff_but():
    staff_but = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for staff in staff_list:
        staff_but.add(
            staff
        )
    staff_but.add(
        "🌃 Вернутся к выбору города",
        "📂 Главное меню"
    )
    return staff_but


def buy_menu():
    buy_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buy_menu.add(
        "♻️ Выбрать район автоматически",
    )
    buy_menu.add(
        "🌃 Вернутся к выбору города",
        "📂 Главное меню"
    )
    return buy_menu





