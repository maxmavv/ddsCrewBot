# -*- coding: utf-8 -*-

#токен бота
token = 'token token tokene'

#приветственное сообщение бота
hello_msg = '''Привет! Я бот для чата DDS. Если тебе это ничего не говорит, иди своей дорогой дальше.
Пока что я умею не очень много чего, но буду расти:
/chto_v_mumu - сегодняшнее меню в МУМУ
/all - пингануть всех в чате
/subscribe - подписаться на рассылку @all
/unsubscribe - отписаться от рассылки @all
'''

#название базы данных пользователей в чатах
db_name = 'bot_database.db'

#сообщение о подписке на бота
subscribe_msg = '''Принято! Ты подписан на рассылку all'''

#сообщение об отписке от бота
unsubscribe_msg = '''Принято! Ты отписан от рассылки all'''

#словарь соответствий номера дня недели и английского/русского названия (для генерации ссылок)
week = {
        0:'ponedelnik',
        1:'vtornik',
        2:'sreda',
        3:'chetverg',
        4:'pyatnitsa',
        5:'subbota',
        6:'-'
        }
week_rus = {
        0:'понедельник',
        1:'вторник',
        2:'среда',
        3:'четверг',
        4:'пятница',
        5:'суббота',
        6:'-'
        }
