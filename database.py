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
            );"""

ct_election_text = """CREATE TABLE IF NOT EXISTS ELECTION
            (
            chat_id integer,
            participant_id integer,
            elec_time integer,
            penalty_time integer
            );"""

ct_election_hist_text = """CREATE TABLE IF NOT EXISTS ELECTION_HIST
            (
            chat_id integer,
            participant_id integer,
            elec_time integer,
            penalty_time integer,
            election_date text
            );"""

ct_chatID_text = """CREATE TABLE IF NOT EXISTS CHAT_ID
            (
            chat_id integer
            );"""

# ins_text = """INSERT INTO PARTICIPANT
#             VALUES ('%d','%d','%s','%s','%s');
#             """

# del_text = """DELETE FROM PARTICIPANT WHERE chat_id = %d and participant_id = %d;
#             """

# del_election_text = """DELETE FROM ELECTION WHERE chat_id = %d and participant_id = %d;
#             """

# sel_all_text = """SELECT * FROM PARTICIPANT WHERE chat_id = %d ;
#                 """

# sel_text = """SELECT * FROM PARTICIPANT WHERE chat_id = %d and participant_id = %d;
#             """

# sel_election_text = """SELECT * FROM ELECTION WHERE chat_id = %d and participant_id = %d;
#                     """

# upd_election_text = """UPDATE ELECTION
#                     set elec_time = %d
#                     WHERE chat_id = %d and participant_id = %d;
#                     """

# reset_election_time_text = """UPDATE ELECTION set elec_time = %d"""

# colect_election_hist_text = """INSERT INTO ELECTION_HIST
#                             SELECT elc.*, cast('%s' as DATE) from ELECTION as elc
#                             """


ins_lj_participant_election_text = """INSERT INTO ELECTION
            SELECT part.chat_id, part.participant_id,
            cast(0 as integer), cast(0 as integer)
            FROM
            PARTICIPANT AS part LEFT JOIN ELECTION as elec
            on (part.chat_id = elec.chat_id and
            part.participant_id = elec.participant_id)
            WHERE elec.participant_id is NULL;"""

# судя по документации библиотеки, использовать ? более секурно, чем %*
ins_text = """INSERT INTO PARTICIPANT
            VALUES (?,?,?,?,?);"""

del_text = """DELETE FROM PARTICIPANT WHERE chat_id = ? and participant_id = ?;"""

del_election_text = """DELETE FROM ELECTION WHERE chat_id = ? and participant_id = ?;"""

sel_all_text = """SELECT * FROM PARTICIPANT WHERE chat_id = ?;"""

sel_text = """SELECT * FROM PARTICIPANT WHERE chat_id = ? and participant_id = ?;"""

sel_election_text = """SELECT * FROM ELECTION WHERE chat_id = ? and participant_id = ?;"""

upd_election_text = """UPDATE ELECTION
                    set elec_time = ?
                    WHERE chat_id = ? and participant_id = ?;"""

reset_election_time_text = """UPDATE ELECTION set elec_time = ?;"""

colect_election_hist_text = """INSERT INTO ELECTION_HIST
                            SELECT elc.*, cast(? as text) FROM ELECTION as elc;"""

sel_chatID_text = """SELECT * FROM CHAT_ID WHERE chat_id = ?;"""

ins_chatID_text = """INSERT INTO CHAT_ID
                    VALUES (?);"""

del_chatID_text = """DELETE FROM CHAT_ID WHERE chat_id = ?;"""

sel_all_chatID_text = """SELECT * FROM CHAT_ID;"""


# создать таблицу
@cfg.loglog(command='create_table', type='ct')
def create_table():
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    # таблица участников
    cursor.execute(ct_text)
    # таблица для голосования
    cursor.execute(ct_election_text)
    # таблица истории голосований
    cursor.execute(ct_election_hist_text)
    # таблица чатов, подписавшихся на рассылку разных сообщений ботом
    cursor.execute(ct_chatID_text)
    db.commit()


# выполнить sql запрос
@cfg.loglog(command='sql_exec', type='db_exec')
def sql_exec(exec_text, params):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    cursor.execute(exec_text, params)
    db.commit()
    return cursor.fetchall()


# очистка таблицы голосования, ТОЛЬКО ДЛЯ ТЕСТИРОВАНИЯ!!!
# sql_exec(reset_election_time_text, [0])
# print(sql_exec("""UPDATE ELECTION set elec_time = %d""", [0]))
# print(sql_exec("""DELETE FROM ELECTION_HIST""", []))

# print(sql_exec(sel_all_text, [cfg.dds_chat_id]))

# print(sql_exec("""DROP TABLE ELECTION_HIST""", []))
# print(sql_exec(colect_election_hist_text, ['2018-09-06']))
# print(sql_exec("""SELECT * FROM ELECTION_HIST""", []))


# вставить данные в таблицу participant and election
@cfg.loglog(command='insert_into_participants', type='db_common')
def insert_into_participants(chat_id, user):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()

    # не добавляем дубли
    cursor.execute(sel_text, [chat_id, user.id])
    if len(cursor.fetchall()) != 0:
        return -1

    cursor.execute(ins_text, [chat_id, user.id, user.first_name, user.last_name, user.username])
    # обновляем таблицу голосующих за обед
    cursor.execute(ins_lj_participant_election_text)
    db.commit()
    return 1


# удалить данные из таблиц participant and election по конкретному чату-клиенту
@cfg.loglog(command='delete_from_participants', type='db_common')
def delete_from_participants(chat_id, user_id):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    cursor.execute(del_text, [chat_id, user_id])
    # удаляем участника из таблицы голосующих за обед
    cursor.execute(del_election_text, [chat_id, user_id])
    db.commit()


# вставить данные в таблицу participant and election
@cfg.loglog(command='insert_into_chatID', type='sql_chatID')
def insert_into_chatID(chat_id):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()

    # не добавляем дубли
    cursor.execute(sel_chatID_text, [chat_id])
    if len(cursor.fetchall()) != 0:
        return -1

    cursor.execute(ins_chatID_text, [chat_id])
    db.commit()
    return 1


# удалить данные из таблиц participant and election по конкретному чату-клиенту
@cfg.loglog(command='delete_from_chatID', type='sql_chatID')
def delete_from_chatID(chat_id):
    db = sql.connect(cfg.db_name)
    cursor = db.cursor()
    cursor.execute(del_chatID_text, [chat_id])
    db.commit()


# создать таблицы, если их нет
create_table()

# обнуляем таблицу голосования
sql_exec(reset_election_time_text, [0])

# обновляем список чатов, чьи сообщения бот может читать
cfg.subscribed_chats_transform(sql_exec(sel_all_chatID_text, []))

# print(sql_exec(sel_all_text, (cfg.dds_chat_id)))


# db = sql.connect(cfg.db_name)
# cursor = db.cursor()
# cursor.execute('''select * from participant;''')
# cursor.execute('''select * from ELECTION;''')
# print(cursor.fetchall())
# db.commit()
