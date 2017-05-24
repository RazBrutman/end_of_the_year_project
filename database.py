import sqlite3
import time
import datetime
import random

conn = sqlite3.connect('database.db')
c = conn.cursor()

def main():
    create_table()
    delete_db()
    dynamic_data_entry()
    for i in range(10):
        dynamic_data_entry()

    c.close()
    conn.close()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS accounts(UserID INT, Username TEXT, Password TEXT)")


def delete_db():
    c.execute("DELETE FROM accounts")


def dynamic_data_entry():

    unix = int(time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    keyword = 'Python'

    c.execute("INSERT INTO accounts (UserID, Username, Password) VALUES (?, ?, ?)", (unix, date, keyword))
    conn.commit()

main()
