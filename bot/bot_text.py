from utils.db_api.baza import*



def profile_text(userid, name):
    info = get_user_info(userid)
    return(f"👨‍💻 <b>Профиль:</b> <code>{name}</code>\n"
    f"🆔 <code>{userid}</code>\n\n"
    f"🏧 <b>Баланс:</b> <code>{info[1]} руб.</code>\n"
    f"📦 <b>Кол-во покупок:</b> <code>{info[2]} шт.</code>\n\n"
    f"📅 <b>Дата регистрации:</b> <code>{info[3]}</code>")



