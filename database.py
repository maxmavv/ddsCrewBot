# -*- coding: utf-8 -*-

import sqlite3 as sql
import config as cfg

ct_text = """CREATE TABLE IF NOT EXISTS PARTICIPANT
            (
            chat_id integer,
            participant_id integer,
            participant_first_name text,
            participant_last_name text,
            participant_username text
            );
            """

ct_election_text = """CREATE TABLE IF NOT EXISTS ELECTION
            (
            chat_id integer,
            participant_id integer,
            elec_time integer,
            penalty_time integer
            );
            """

ct_election_hist_text = """CREATE TABLE IF NOT EXISTS ELECTION_HIST
            (
            chat_id integer,
            participant_id integer,
            elec_time integer,
            penalty_time integer,
            election_date date
            );
            """

ins_lj_participant_election_text = """INSERT INTO ELECTION
            select part.chat_id, part.participant_id,
            cast(0 as integer), cast(0 as integer)
            from
            PARTICIPANT AS part LEFT JOIN ELECTION as elec
            on (part.chat_id = elec.chat_id and
            part.participant_id = elec.participant_id)
            where elec.participant_id is NULL
            """

ins_text = """INSERT INTO PARTICIPANT
            VALUES ('%d','%d','%s','%s','%s');
            """

del_text = """DELETE FROM PARTICIPANT WHERE chat_id = %d and participant_id = %d;
            """

del_election_text = """DELETE FROM ELECTION WHERE chat_id = %d and participant_id = %d;
            """

sel_all_text = """SELECT * FROM PARTICIPANT WHERE chat_id = %d ;
            """

sel_text = """SELECT * FROM PARTICIPANT WHERE chat_id = %d and participant_id = %d;
            """

sel_election_text = """SELECT * FROM ELECTION WHERE chat_id = %d and participant_id = %d;
            """

upd_election_text = """UPDATE ELECTION
            set elec_time = %d
            WHERE chat_id = %d and participant_id = %d;
            """


# создать таблицу
def create_table():
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    # таблица участников
    cursor.execute(ct_text)
    # таблица для голосования
    cursor.execute(ct_election_text)
    # таблица истории голосований
    cursor.execute(ct_election_hist_text)
    db.commit()


# выполнить sql запрос
def sql_exec(select_text, params):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    cursor.execute(select_text % params)
    db.commit()
    return cursor.fetchall()


# очистка таблицы голосования, ТОЛЬКО ДЛЯ ТЕСТИРОВАНИЯ!!!
# print(sql_exec("""UPDATE ELECTION set elec_time = %d""", (0)))


# вставить данные в таблицу participant and election
def insert_into_table(chat_id, user):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()

    # не добавляем дубли
    cursor.execute(sel_text % (chat_id, user.id))
    if len(cursor.fetchall()) != 0:
        return -1

    cursor.execute(ins_text % (chat_id, user.id, user.first_name, user.last_name, user.username))
    # обновляем таблицу голосующих за обед
    cursor.execute(ins_lj_participant_election_text)
    db.commit()
    return 1


# удалить данные из таблиц participant and election по конкретному чату-клиенту
def delete_from_table(chat_id, user_id):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    cursor.execute(del_text % (chat_id, user_id))
    # удаляем участника из таблицы голосующих за обед
    cursor.execute(del_election_text % (chat_id, user_id))
    db.commit()


# создать таблицы, если их нет
create_table()

# print(sql_exec(sel_all_text, (cfg.dds_chat_id)))


# db = sql.connect(cfg.db_name)
# cursor = db.cursor()
# cursor.execute('''select * from participant;''')
# cursor.execute('''select * from ELECTION;''')
# print(cursor.fetchall())
# db.commit()
