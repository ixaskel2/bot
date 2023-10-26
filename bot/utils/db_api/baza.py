import sqlite3
import logging




def check_new_user(userid):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        check = q.execute(f"SELECT * FROM users WHERE id = {int(userid)}").fetchone()
        connect.commit()
        if check is None:
            return True
        else:
            return False
            
    except Exception as err:
        logging.exception(err)
        return err




def add_new_user(userid, date):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        q.execute("INSERT INTO users(id, balance,count,date, ban) VALUES ('%s', '%s', '%s', '%s', '%s')"%(userid, 0.0, 0, date, 0))
        connect.commit()
        return True
        
    except Exception as err:
        return err


def get_user_info(userid):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        info = q.execute(f"SELECT * FROM users WHERE id = {int(userid)}").fetchone()
        return info
    except Exception as err:
        return err
    
def admins_setting_info():
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        settings = q.execute("SELECT * FROM admin_settings").fetchone()
        if settings is None:
            q.execute("INSERT INTO admin_settings(p2p, btc, usdt) VALUES ('%s', '%s', '%s')"%(0,0,0))
            connect.commit()
        else:
            return settings
        
    except Exception as err:
        logging.exception(err)



def add_balance(userid, amount):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        balance = q.execute(f"SELECT balance FROM users WHERE id = {userid}").fetchone()[0]
        new_balance = int(balance) + int(amount)
        q.execute(f"update users set balance = {new_balance} where id = {userid}")
        connect.commit()
        return True
        
    except Exception as err:
        logging.exception(err)


def minus_balance(userid, amount):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        balance = q.execute(f"SELECT balance FROM users WHERE id = {userid}").fetchone()[0]
        new_balance = int(balance) - int(amount)
        q.execute(f"update users set balance = {new_balance} where id = {userid}")
        connect.commit()
        return True
        
    except Exception as err:
        logging.exception(err)

def add_new_buy(userid, staff_id, summa, btc_summa, staff, type_klad, city, date):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        q.execute("INSERT INTO busket_info(id, staff_id, summa, btc_summa, staff, type_klad, city, date) VALUES ('%s','%s','%s','%s','%s','%s','%s', '%s')"%(userid, staff_id, summa, btc_summa, staff, type_klad, city, date))
        connect.commit()
        return True
    except Exception as err:
        logging.exception(err)

def get_busket_info(userid):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        info = q.execute(f"SELECT staff_id FROM busket_info WHERE id = {int(userid)}").fetchall()
        return info
    except Exception as err:
        logging.exception(err)


def staff_info(staff_id):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        info = q.execute(f"SELECT * FROM busket_info WHERE staff_id = '{staff_id}'").fetchone()
        return info
    
    except Exception as err:
        logging.exception(err)


def delete_basket(staff_id):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        q.execute(f"DELETE FROM busket_info WHERE staff_id = '{staff_id}'")
        connect.commit()
        return True
    except Exception as err:
        logging.exception(err)



def all_buscket():
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        info = q.execute("SELECT staff_id FROM busket_info").fetchall()
        return info
    
    except Exception as err:
        logging.exception(err)

def users_id_for_spam():
    connect = sqlite3.connect("data/data.db")
    q = connect.cursor()
    users = q.execute("SELECT id FROM users").fetchall()
    return users

def clear_bd(userid):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        q.execute(f"DELETE FROM users WHERE id = {userid}")
        connect.commit()
        return True
    except Exception as err:
        logging.exception(err)


def set_p2p(key):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        q.execute(f"update admin_settings set p2p = '{key}'")
        connect.commit()
        return True
    except Exception as err:
        logging.exception(err)

def set_btc(btc):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        q.execute(f"update admin_settings set btc = '{btc}'")
        connect.commit()
        return True
    except Exception as err:
        logging.exception(err)

def set_usdt(usdt):
    try:
        connect = sqlite3.connect("data/data.db")
        q = connect.cursor()
        q.execute(f"update admin_settings set usdt = '{usdt}'")
        connect.commit()
        return True
    except Exception as err:
        logging.exception(err)

def count_users():
    connect = sqlite3.connect("data/data.db")
    q = connect.cursor()
    counter = q.execute("SELECT COUNT(id) FROM users").fetchone()[0]
    connect.commit()
    return counter