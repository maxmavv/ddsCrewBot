# -*- coding: utf-8 -*-
import config as cfg
import text_processing as tp
import mumu
import telebot
import time
import datetime
import database as db
import random
import event_timer as evt
import webhook

random.seed(time.clock())

bot = telebot.TeleBot(cfg.token)

# week_day = datetime.datetime.today().weekday()

# определяем дефолтное время
dinner_time = cfg.dinner_default_time
dinner_time = datetime.timedelta(hours=dinner_time[0], minutes=dinner_time[1])
cfg.show_din_time = str(dinner_time)[:-3]

# таймеры
# evt.dinner_time_timer(bot)
evt.one_hour_timer(bot)


# приветствие
@bot.message_handler(commands=['start', 'help'])
@cfg.loglog(command='start/help', type='message')
def send_welcome(message):
    cid = message.chat.id
    bot.send_message(cid, cfg.hello_msg)


# меню в муму
@bot.message_handler(commands=['chto_v_mumu'])
@cfg.loglog(command='chto_v_mumu', type='message')
def send_mumu(message):
    cid = message.chat.id
    week_day = datetime.datetime.today().weekday()
    lunches = mumu.lunches(week_day)

    bot.send_message(cid, lunches[0][0])
    bot.send_message(cid, lunches[0][1])
    bot.send_message(cid, lunches[1][0])
    bot.send_message(cid, lunches[1][1])


# регистрируем человека в списке участников чата по его запросу
@bot.message_handler(commands=['subscribe'])
@cfg.loglog(command='subscribe', type='message')
def subscribe(message):
    cid = message.chat.id
    user = message.from_user
    res = db.insert_into_participants(cid, user)
    if res == -1:
        bot.send_message(cid, cfg.err_subscribe_msg)
    else:
        bot.send_message(cid, cfg.subscribe_msg)


# удаляем человека из списка участников чата по его запросу
@bot.message_handler(commands=['unsubscribe'])
@cfg.loglog(command='unsubscribe', type='message')
def unsubscribe(message):
    cid = message.chat.id
    user_id = message.from_user.id
    db.delete_from_participants(cid, user_id)
    bot.send_message(cid, cfg.unsubscribe_msg)


# регистрируем чат в рассылки на сообщения ботом
@bot.message_handler(commands=['admin_subscribe_for_messages'])
@cfg.loglog(command='admin_subscribe_for_messages', type='message')
def admin_subscribe_for_dinner(message):
    cid = message.chat.id
    res = db.insert_into_chatID(cid)
    if res == -1:
        bot.send_message(cid, cfg.err_subscribe_msg_chatId)
    else:
        bot.send_message(cid, cfg.subscribe_msg_chatId)


# удаляем чат из рассылки на сообщения ботом
@bot.message_handler(commands=['admin_unsubscribe_for_messages'])
@cfg.loglog(command='admin_unsubscribe_for_messages', type='message')
def admin_unsubscribe_for_dinner(message):
    cid = message.chat.id
    db.delete_from_chatID(cid)
    bot.send_message(cid, cfg.unsubscribe_msg_chatId)


# призвать всех
@bot.message_handler(commands=['all'])
@cfg.loglog(command='all', type='message')
def ping_all(message):
    cid = message.chat.id
    user_id = message.from_user.id
    users = db.sql_exec(db.sel_all_text, [cid])
    call_text = 'Эй, @all: '
    # бежим по всем юзерам в чате
    for i in users:
        # если юзер не тот, кто вызывал all, уведомляем его
        if i[1] != user_id:
            call_text = call_text + '@' + str(i[4]) + ' '

    # проверка на /all@ddsCrewBot
    if (message.text[0:15] == '/all@ddsCrewBot'):
        bot.send_message(cid, call_text.strip() + message.text[15:])
    else:
        bot.send_message(cid, call_text.strip() + message.text[4:])


# подбросить монетку
@bot.message_handler(commands=['coin'])
@cfg.loglog(command='coin', type='message')
def throw_coin(message):
    cid = message.chat.id
    bot.send_message(cid, random.choice(cfg.precomand_text))
    time.sleep(1)

    bot.send_message(cid, random.choice(cfg.coin_var))


# подбросить кубик
@bot.message_handler(commands=['dice'])
@cfg.loglog(command='dice', type='message')
def throw_dice(message):
    cid = message.chat.id
    bot.send_message(cid, random.choice(cfg.precomand_text))
    time.sleep(1)

    if len(message.text.split()) == 2 and message.text.split()[1].isdigit():
        bot.send_message(cid, random.randint(1, int(message.text.split()[1])))
    else:
        bot.send_message(cid, random.choice(cfg.dice_var))


# магический шар
@bot.message_handler(commands=['ball'])
@cfg.loglog(command='ball', type='message')
def magic_ball(message):
    cid = message.chat.id
    bot.send_message(cid, random.choice(cfg.ball_var))


# показать время обеда
# @bot.message_handler(commands=['dinner'])
# def show_dinner_time(message):
#     cid = message.chat.id
#     bot.send_message(cid, str(dinner_time)[:-3])


# раскомментировать, чтобы узнать file_id стикера
# @bot.message_handler(content_types=["sticker"])
# def get_stiker(message):
#     print(message.sticker.file_id)
#     cid = message.chat.id
#     bot.send_sticker(cid, 'CAADBAADcAAD-OAEAsKXeIPkd1o3Ag')


@bot.message_handler(content_types=["text"])
def text_parser(message):
    print('##########', datetime.datetime.now(), 'text_parser')

    week_day = datetime.datetime.today().weekday()
    # нужно брать дату из даты сообщения
    hour_msg = time.localtime(message.date).tm_hour
    # текущее время, может пригодиться
    # hour_now = time.localtime().tm_hour
    cid = message.chat.id

    if cid in cfg.subscribed_chats:
        user_id = message.from_user.id

        # # лол кек ахахаха детектор
        if tp.lol_kek_detector(message.text) is True:
            print('##########', datetime.datetime.now(), 'lol_kek_detector')

            if random.random() >= 0.8:
                bot.send_sticker(cid, cfg.stiker_kot_eban)
                print('Sent!')

        # # голосование за обед
        din_elec = tp.dinner_election(message.text)
        # ТОЛЬКО ДЛЯ ТЕСТИРОВАНИЯ!!!
        # if din_elec is not False:
        if week_day not in (5, 6) and hour_msg < 12 and din_elec is not False:
            print('##########', datetime.datetime.now(), 'dinner_election')

            print('Din_elec =', din_elec)
            user = db.sql_exec(db.sel_election_text, [cid, user_id])
            if len(user) == 0:
                bot.reply_to(message, cfg.err_vote_msg)
            else:
                global dinner_time
                elec_time = datetime.timedelta(minutes=din_elec)
                dinner_time += elec_time

                # голосование или переголосование
                if int(user[0][2]) == 0:
                    bot.reply_to(message, cfg.vote_msg + str(dinner_time)[:-3])
                else:
                    elec_time = datetime.timedelta(minutes=int(user[0][2]))
                    dinner_time -= elec_time
                    bot.reply_to(message, cfg.revote_msg + str(dinner_time)[:-3])

                cfg.show_din_time = str(dinner_time)[:-3]
                print('Время обеда', cfg.show_din_time)
                db.sql_exec(db.upd_election_text, [din_elec, cid, user_id])

        # # понеделбник - денб без мягкого знака
        if week_day == 0 and hour_msg < 12 and tp.soft_sign(message.text) is True:
            print('##########', datetime.datetime.now(), 'soft_sign')

            bot.reply_to(message, 'ШТРАФ')
            print('ШТРАФ')

        print('Chat_id =', cid)
        print('User =', user_id)
        print('##########', datetime.datetime.now(), '\n')


print('here')
webhook.webhook(bot)
print('here again')
