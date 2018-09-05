# -*- coding: utf-8 -*-

import sqlite3 as sql
import config as cfg

ct_text = """CREATE TABLE PARTICIPANT
            (
            chat_id integer,
            participant_id integer,
            participant_first_name text,
            participant_last_name text,
            participant_username text
            );
            """

ins_text = """INSERT INTO PARTICIPANT
            VALUES ('%d','%d','%s','%s','%s');
            """

del_text = """DELETE FROM PARTICIPANT WHERE chat_id = %d and participant_id = %d;
            """


sel_all_text = """SELECT * FROM PARTICIPANT WHERE chat_id = %d ;
            """


sel_text = """SELECT * FROM PARTICIPANT WHERE chat_id = %d and participant_id = %d;
            """


# создать таблицу
def create_table():
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    cursor.execute(ct_text)
    db.commit()


# выбрать данные из таблицы по конкретному чату-клиенту и юзеру
def select_from_table(chat_id, user_id):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    cursor.execute(sel_text % (chat_id, user_id))
    db.commit()
    return cursor.fetchall()


# вставить данные в таблицу
def insert_into_table(chat_id, user):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()

    # не добавляем дубли
    cursor.execute(sel_text % (chat_id, user.id))
    if len(cursor.fetchall()) != 0:
        return -1

    cursor.execute(ins_text % (chat_id, user.id, user.first_name, user.last_name, user.username))
    db.commit()
    return 1


# удалить данные из таблицы по конкретному чату-клиенту
def delete_from_table(chat_id, user_id):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    cursor.execute(del_text % (chat_id, user_id))
    db.commit()


# выбрать данные из таблицы по конкретному чату-клиенту
def select_all_from_table(chat_id):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    cursor.execute(sel_all_text % (chat_id))
    db.commit()
    return cursor.fetchall()


# create_table()
# select_from_table('')


db = sql.connect(cfg.db_name)
cursor = db.cursor()
# cursor.execute('''select * from participant;''')
# print(cursor.fetchall())
db.commit()
