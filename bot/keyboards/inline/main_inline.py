from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api.baza import*

def start_menu():
    start_menu = InlineKeyboardMarkup(row_width=1)
    start_menu.add(
        InlineKeyboardButton(text="📃 Правила шопа", url="https://telegra.ph/HOT-TROPICS-RULES-10-25"),
        InlineKeyboardButton(text="☑️ Ознакомлен", callback_data="accept_rules")
    )
    return start_menu

def profile_but(userid):
    profile_but = InlineKeyboardMarkup(row_width=2)
    profile_but.add(
        InlineKeyboardButton(text="🗑 Корзина({} шт.)".format(len(get_busket_info(userid))), callback_data="basket"),
        InlineKeyboardButton(text="🛒 Мои покупки", callback_data="my_buys"),
        InlineKeyboardButton(text="📥 Пополнить баланс", callback_data="add_balance"),
    )
    return profile_but

def payment_menu():
    payment_menu = InlineKeyboardMarkup(row_width=2)
    payment_menu.add(
        InlineKeyboardButton(text="💳 Пополнить картой", callback_data="add_qiwi"),
       #  InlineKeyboardButton(text="🧾 Оплатить по реквизитам", callback_data="from_req+{}+{}".format(staff_id, bill_id)),
       # InlineKeyboardButton(text="🤖 BTC banker", callback_data="add_banker"),
        InlineKeyboardButton(text="💮 BTC", callback_data="add_btc"),
        InlineKeyboardButton(text="🪙 USDT", callback_data="add_usdt"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_profile"),
    )
    return payment_menu

def cancel_payment():
    cancel_payment = InlineKeyboardMarkup()
    cancel_payment.add(
        InlineKeyboardButton(text="💢 Отменить", callback_data="cancel_payment")
    )
    return cancel_payment

def pay_link_button(link, bill_id, amount):
    pay_link_button = InlineKeyboardMarkup(row_width=2)
    pay_link_button.add(
        InlineKeyboardButton(text="🤵‍♂️ Оператор SUPPORT", url="https://t.me/operator_tropics"),
    )
    pay_link_button.add(
       # InlineKeyboardButton(text="👍 Я оплатил", callback_data="payed+{}+{}".format(bill_id, amount)),
       InlineKeyboardButton(text="👍 Я оплатил",  callback_data="check_pay"),
    #    InlineKeyboardButton(text="🔍 Проверить оплату", callback_data="check_pay"),
        InlineKeyboardButton(text="👎 Отменить", callback_data="reject_payment+{}".format(bill_id))
    )
    return pay_link_button


def busket_but(info):
    busket_but = InlineKeyboardMarkup(row_width=1)
    for i in info:
        busket_but.add(
            InlineKeyboardButton(text=f"🧿 Товар #{i[0]}", callback_data="staff+{}".format(i[0]))
        )
    
    busket_but.add(
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_profile"),
    )
    return busket_but


def pay_menu(staff_id, link, bill_id):
    pay_menu = InlineKeyboardMarkup(row_width=2)
    pay_menu.add(
        InlineKeyboardButton(text="🔰Оплатить с баланса", callback_data="from_balance+{}".format(staff_id)),
     #   InlineKeyboardButton(text="🥝 Qiwi |💳 Карта", url=f"{link}"),
        InlineKeyboardButton(text="💮 BTC", callback_data="from_btc+{}+{}".format(staff_id, bill_id)),
     #   InlineKeyboardButton(text="🪙 USDT", callback_data="from_usdt+{}+{}".format(staff_id, bill_id)),
        InlineKeyboardButton(text="💳 Оплата картой ", callback_data="from_req+{}+{}".format(staff_id, bill_id)),
        InlineKeyboardButton(text="🧛‍♀️ Скрыть", callback_data="hide_buy+{}".format(bill_id)),
        InlineKeyboardButton(text="💢 Отменить", callback_data="cancel_pay+{}+{}".format(bill_id, staff_id)),
    )
    return pay_menu


def auto_rayon(userid):
    auto_rayon = InlineKeyboardMarkup()
    auto_rayon.add(
        InlineKeyboardButton(text="♻️ Авто-район", callback_data="auto+{}".format(userid))
    )
    return auto_rayon

def support_but():
    support_but = InlineKeyboardMarkup(row_width=1)
    support_but.add(
        InlineKeyboardButton(text="🤵‍♂️ Оператор SUPPORT", url="https://t.me/operator_tropics"),
        InlineKeyboardButton(text=" TROPICS Работа ", url="https://t.me/tropics_job"),
    #    InlineKeyboardButton(text="📣 Наш Канал с новостями 📣", url="https://t.me/tropicshot")
      
    )
    return support_but


def svyr_but():
    support_but = InlineKeyboardMarkup(row_width=1)
    support_but.add(
        InlineKeyboardButton(text="🚑 Бот первой помощи", url="https://t.me/megahealth_bot"),
      #  InlineKeyboardButton(text="💬 Чат антишвыр", url="https://t.me/cartel_adminbot")
    )
    return support_but

def check_payment_but():
    check_payment = InlineKeyboardMarkup(row_width=1)
    check_payment.add(
        InlineKeyboardButton(text="🔍 Проверить оплату", callback_data="check_pay"),
        InlineKeyboardButton(text="🤵‍♂️ Оператор SUPPORT", url="https://t.me/operator_tropics"),
        InlineKeyboardButton(text="💢 Отменить", callback_data="cancel_payment"),
    )
    return check_payment