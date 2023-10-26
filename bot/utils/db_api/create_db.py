import sqlite3


def create_db():
    connect = sqlite3.connect("data/data.db")
    q = connect.cursor()
    q.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER,
        balance REAL,
        count INTEGER,
        date TEXT,
        ban INTEGER
    )""")
    q.execute("""CREATE TABLE IF NOT EXISTS admin_settings(
        p2p TEXT,
        btc TEXT,
        usdt TEXT
    )""")
    q.execute("""CREATE TABLE IF NOT EXISTS busket_info(
        id INTEGER,
        staff_id TEXT,
        summa INTEGER,
        btc_summa REAL,
        staff TEXT,
        type_klad TEXT,
        city TEXT,
        date TEXT

    )""")
    connect.commit()
    return True

