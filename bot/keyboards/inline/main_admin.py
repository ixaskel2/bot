from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def admin_but():
    admin_but = InlineKeyboardMarkup(row_width=2)
    admin_but.add(
        InlineKeyboardButton(text="⚒ BTC", callback_data="set_btc"),
        InlineKeyboardButton(text="⚒ P2P", callback_data="set_p2p"),
        InlineKeyboardButton(text="⚒ USDT", callback_data="set_usdt"),
        InlineKeyboardButton(text="🔔 Рассылка", callback_data="spam"),
        InlineKeyboardButton(text="📊 Статистика", callback_data="stata"),
        InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings"),
        InlineKeyboardButton(text="🧛‍♀️ Скрыть", callback_data="hide_adm"),
    )
    return admin_but


def spam_types():
    spam_types = InlineKeyboardMarkup(row_width=2)
    spam_types.add(
        InlineKeyboardButton(text="💬 Текстом", callback_data="spam_text"),
        InlineKeyboardButton(text="🌌 Картинкой", callback_data="spam_pic"),
        InlineKeyboardButton(text="📹 Видео", callback_data="spam_video"),
        InlineKeyboardButton(text="🎑 Гифкой", callback_data="spam_gif"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_admin"),
    )
    return spam_types


def cancel_but():
    cancel_but = InlineKeyboardMarkup()
    cancel_but.add(
        InlineKeyboardButton(text="💢 Отменить", callback_data="cansel_spam")
    )
    return cancel_but


def spam_withot_but():
    spam_withot_but = InlineKeyboardMarkup()
    spam_withot_but.add(
        InlineKeyboardButton(text="💢 Понятно", callback_data="close_spam")
    )
    return spam_withot_but

def spam_with_but(text, url):
    spam_with_but = InlineKeyboardMarkup(1)
    spam_with_but.add(
        InlineKeyboardButton(text="{}".format(text), url="{}".format(url)),
        InlineKeyboardButton(text="💢 Понятно", callback_data="close_spam")
    )
    return spam_with_but

