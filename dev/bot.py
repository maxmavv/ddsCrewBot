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
import adminId

random.seed(time.clock())

bot = telebot.TeleBot(cfg.token)

# week_day = datetime.datetime.today().weekday()

# определяем дефолтное время
cfg.dinner_time = cfg.dinner_default_time
cfg.dinner_time = datetime.timedelta(hours=cfg.dinner_time[0], minutes=cfg.dinner_time[1])
cfg.show_din_time = str(cfg.dinner_time)[:-3]

# таймеры
# evt.dinner_time_timer(bot)
evt.one_hour_timer(bot)
evt.check_metadata(bot)

# time_now = datetime.datetime.now()
# hh = random.randint(1, 119)
# mm = random.randint(1, 58)
# ss = random.randint(0, 50)

# hh = 0
# mm = 0
# ss = 10


# # вычисляем дату исполнения
# delta = datetime.timedelta(hours=hh, minutes=mm, seconds=ss)
# expire_date = time_now + delta

# for cid in cfg.subscribed_chats:
#     users = db.sql_exec(db.sel_all_text, [cid])
#     if users != []:
#         call_user = '@' + random.choice(users)[4]
#         call_user = random.choice(users)[1]

#         # добавляем строку воронкова в метаданные для каждого чата
#         db.sql_exec(db.ins_operation_meta_text,
#                     [cfg.max_id_rk, 1, cid, call_user, -1,
#                      str(time_now)[:-7], str(expire_date)[:-7], 1])
#         cfg.max_id_rk += 1


# hh = 0
# mm = 0
# ss = -10


# # вычисляем дату исполнения
# delta = datetime.timedelta(hours=hh, minutes=mm, seconds=ss)
# expire_date = time_now + delta

# for cid in cfg.subscribed_chats:
#     users = db.sql_exec(db.sel_all_text, (cid,))
#     if users != []:
#         call_user = random.choice(users)[1]

#         # добавляем строку воронкова в метаданные для каждого чата
#         db.sql_exec(db.ins_operation_meta_text,
#                     [cfg.max_id_rk, 1, cid, call_user, -1,
#                      str(time_now)[:-7], str(expire_date)[:-7], 1])
#          cfg.max_id_rk += 1
# evt.check_metadata(bot)


# стучимся к серверам ТГ, если не пускает
def telegram_polling():
    try:
        # constantly get messages from Telegram
        bot.polling(none_stop=True, timeout=60)
        print('ok')
    except Exception as e:
        # print(e)
        bot.stop_polling()
        time.sleep(10)
        print('try...')
        telegram_polling()


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
    bot.send_chat_action(cid, 'typing')
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
    bot.send_chat_action(cid, 'typing')
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
    bot.send_chat_action(cid, 'typing')
    user_id = message.from_user.id
    db.delete_from_participants(cid, user_id)
    bot.send_message(cid, cfg.unsubscribe_msg)


# регистрируем чат в рассылки на сообщения ботом
@bot.message_handler(commands=['admin_subscribe_chat'])
@cfg.loglog(command='admin_subscribe_chat', type='message')
def admin_subscribe_chat(message):
    cid = message.chat.id
    res = db.insert_into_chatID(cid)
    if res == -1:
        bot.send_message(cid, cfg.err_subscribe_msg_chatId)
    else:
        bot.send_message(cid, cfg.subscribe_msg_chatId)


# удаляем чат из рассылки на сообщения ботом
@bot.message_handler(commands=['admin_unsubscribe_chat'])
@cfg.loglog(command='admin_unsubscribe_chat', type='message')
def admin_unsubscribe_chat(message):
    cid = message.chat.id
    db.delete_from_chatID(cid)
    bot.send_message(cid, cfg.unsubscribe_msg_chatId)


# призвать всех
@bot.message_handler(commands=['all'])
@cfg.loglog(command='all', type='message')
def ping_all(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')
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
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)

    bot.send_message(cid, random.choice(cfg.coin_var))


# подбросить кубик
@bot.message_handler(commands=['dice'])
@cfg.loglog(command='dice', type='message')
def throw_dice(message):
    cid = message.chat.id
    bot.send_message(cid, random.choice(cfg.precomand_text))
    bot.send_chat_action(cid, 'typing')
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
    bot.send_message(cid, random.choice(cfg.precomand_ball))
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)

    bot.reply_to(message, random.choice(cfg.ball_var))


# показать время обеда
@bot.message_handler(commands=['dinner'])
@cfg.loglog(command='dinner', type='message')
def show_dinner_time(message):
    cid = message.chat.id
    bot.send_message(cid, random.choice(cfg.dinner_text) + cfg.show_din_time)


# сделать SQL запрос
@bot.message_handler(commands=['sqlsql'])
@cfg.loglog(command='sqlsql', type='message')
def sqlsql(message):
    cid = message.chat.id
    user = message.from_user.id
    bot.send_chat_action(cid, 'typing')

    sqlQuery = message.text[8:]
    print(sqlQuery)

    if sqlQuery.find(';') != -1:
        bot.send_message(cid, 'Запрос надо писать без ";"!')
    else:
        # if sqlQuery.upper().startswith('SELECT'):
        if user == adminId.adminId:
            res = db.sql_exec(sqlQuery, [])
            # print(str(res))
            resStr = '[]'
            if res == 'ERROR!':
                resStr = 'Ошибка в SQL запросе!'
            else:
                for i in res:
                    resStr += str(i) + '\n'
            bot.send_message(cid, str(resStr))
        else:
            bot.send_message(cid, 'Извините, онолитики, я выполняю выполняю только запросы разработчика!')
            # bot.send_message(cid, 'Я выполняю только SELECT запросы!')


# показать/оставить штрафы
@bot.message_handler(commands=['penalty'])
@cfg.loglog(command='penalty', type='message')
def penalty(message):
    time_now = datetime.datetime.now()
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')
    pen = db.sql_exec(db.sel_all_penalty_time_text, [cid])
    # pen = db.sql_exec(db.sel_all_penalty_time_text, [-282255340])
    # print(pen)
    # print(db.sql_exec(db.sel_all_text, [-282255340]))
    cmd = message.text.split()
    flg = 0

    if (len(cmd) == 3) and (cmd[1].lower() == 'cancel') and (cmd[2].isdigit()):
        # отмена штрафа
        rk = int(cmd[2])
        meta = db.sql_exec("""SELECT * FROM METADATA WHERE id_rk = ?""", [rk])

        if len(meta) == 0:
            bot.send_message(cid, 'Штрафа с таким номером не существует!')
        else:
            meta = meta[0]
            dttm = datetime.datetime.strptime(meta[5], '%Y-%m-%d %H:%M:%S')
            val = int(meta[4])
            sign = val / abs(val)

            # 1(active) = 1(positive penalty)
            if (dttm.date() == time_now.date()) and (meta[7] == sign):
                if meta[3] == message.from_user.id:
                    bot.send_message(cid, cfg.self_penalty.format('отменять'))
                else:
                    db.sql_exec(db.upd_operation_meta_text, [3, rk])
                    bot.send_message(cid, cfg.cancel_penalty.format(rk))
            else:
                bot.send_message(cid, 'Данный штраф уже невозможно отменить!')
    elif (len(cmd) == 3) and (not cmd[1].isdigit()) and (cmd[2].isdigit()):
        # постановка штрафа
        for user in pen:
            if user[0] == cmd[1][1:]:
                flg = 1

                if user[2] == message.from_user.id:
                    bot.send_message(cid, cfg.self_penalty.format('ставить'))
                    break

                penalty_time = abs(int(cmd[2]))
                if penalty_time != 0:
                    if penalty_time > 25:
                        bot.send_message(cid, 'Я не ставлю штрафы больше чем на 25 минут!')
                    else:
                        # добавляем строку штрафа в метаданные
                        delta = datetime.timedelta(hours=24)
                        # delta = datetime.timedelta(seconds=10)
                        expire_date = time_now + delta

                        db.sql_exec(db.ins_operation_meta_text,
                                    [cfg.max_id_rk, 0, cid, user[2], penalty_time,
                                     str(time_now)[:-7], str(expire_date)[:-7], 1])
                        cfg.max_id_rk += 1

                        bot.send_message(cid, cfg.set_penalty.format(str(cmd[1]),
                                                                     str(penalty_time), cfg.max_id_rk - 1))
                        # evt.check_metadata(bot)
                        # evt.check_metadata(bot)

                        # print(db.sql_exec("""SELECT * FROM ELECTION""", []))
                else:
                    bot.send_message(cid, 'Я не ставлю штрафы 0 минут!')
                break

        if flg == 0:
            bot.send_message(cid, cfg.no_member.format(str(cmd[1])))
    else:
        # вывод списка штрафов
        pen_msg = 'Штрафы на сегодня:\n'
        pen_msg_flg = 0
        for user in pen:
            if int(user[1]) != 0:
                pen_msg += str(user[0]) + ' — ' + str(user[1]) + ' мин\n'
                pen_msg_flg = 1

        if pen_msg_flg == 1:
            bot.send_message(cid, pen_msg)
        else:
            bot.send_message(cid, random.choice(cfg.penalty_empty_text))


# добавить мем
@bot.message_handler(commands=['meme_add'])
@cfg.loglog(command='meme_add', type='message')
def meme_add(message):
    cid = message.chat.id
    user = message.from_user.id
    bot.send_chat_action(cid, 'typing')

    meme_query = message.text.lower().split()
    mem = db.sql_exec(db.sel_meme_text, [cid, meme_query[-1]])
    print(mem)
    print(message)

    # comand
    # if len(meme_query) == 3:
    #     if len(mem) == 0:
    #         db.sql_exec(db.ins_meme_text, [cid, meme_query[-1], type, value])


# удалить мем
# @bot.message_handler(commands=['meme_del'])
# @cfg.loglog(command='meme_del', type='message')
# def meme_del(message):
#     cid = message.chat.id
#     bot.send_chat_action(cid, 'typing')

#     meme_query = message.text.lower().split()

#     if len(meme_query) != 2:
#         bot.send_message(cid, 'Для удаления мне нужно только название!')
#     else:
#         db.sql_exec(db.del_meme_text, [cid, meme_query[-1]])
#         bot.send_message(cid, 'Если такой мем и был, то он удалён!')


# мемы
@bot.message_handler(commands=['meme'])
@cfg.loglog(command='meme', type='message')
def meme(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')

    meme_query = message.text.lower().split()

    if len(meme_query) != 2:
        bot.send_message(cid, 'Мне нужно только название мема!')
    else:
        mem = db.sql_exec(db.sel_meme_text, [cid, meme_query[-1]])
        if len(mem) == 0:
            bot.send_message(cid, 'Мема с таким названием не существует!')
        else:
            bot.send_message(cid, mem[3])


# раскомментировать, чтобы узнать file_id фотографии
@bot.message_handler(content_types=["photo"])
def get_photo(message):
    # print(message)
    # print(str(message.json['photo']))
    print(message.json['photo'][2]['file_id'])
    cid = message.chat.id


# раскомментировать, чтобы узнать file_id стикера
# @bot.message_handler(content_types=["sticker"])
# def get_sticker(message):
#     print(message.sticker.file_id)
#     cid = message.chat.id
#     bot.send_sticker(cid, random.choice(cfg.sticker_var))

@bot.message_handler(content_types=["text"])
@cfg.loglog(command='text_parser', type='message')
def text_parser(message):
    week_day = datetime.datetime.today().weekday()
    # нужно брать дату из даты сообщения
    hour_msg = time.localtime(message.date).tm_hour
    # текущее время, может пригодиться
    # hour_now = time.localtime().tm_hour
    cid = message.chat.id
    user_id = message.from_user.id

    if cid in cfg.subscribed_chats:
        # # лол кек ахахаха детектор
        if tp.lol_kek_detector(message.text) is True:
            print('##########', datetime.datetime.now(), 'lol_kek_detector')

            if random.random() >= 0.8:
                bot.send_sticker(cid, random.choice(cfg.sticker_var))
                print('Sent!')

        # # голосование за обед
        din_elec = tp.dinner_election(message.text)
        # ТОЛЬКО ДЛЯ ТЕСТИРОВАНИЯ!!!
        # if din_elec is not False:
        if week_day not in (5, 6) and hour_msg < 12 and din_elec is not False:
            bot.send_chat_action(cid, 'typing')
            print('##########', datetime.datetime.now(), 'dinner_election')

            print('Din_elec =', din_elec)
            user = db.sql_exec(db.sel_election_text, [cid, user_id])
            if len(user) == 0:
                bot.reply_to(message, cfg.err_vote_msg)
            else:
                penalty_time = int(user[0][3])

                final_elec_time = 0
                sign = 1

                if din_elec != 0:
                    sign = din_elec / abs(din_elec)
                    final_elec_time = din_elec - sign * penalty_time

                if abs(final_elec_time) > 25:
                    final_elec_time = sign * 25

                if sign * final_elec_time < 0:
                    final_elec_time = 0

                # elec_time = datetime.timedelta(minutes=din_elec)
                # cfg.dinner_time += elec_time
                final_elec_time = datetime.timedelta(minutes=final_elec_time)
                cfg.dinner_time += final_elec_time

                additional_msg = ''
                if penalty_time != 0:
                    additional_msg = 'с учётом штрафов '

                # голосование или переголосование
                if int(user[0][2]) == 0:
                    bot.reply_to(message, cfg.vote_msg + additional_msg + str(cfg.dinner_time)[:-3])
                else:
                    final_elec_time = 0
                    prev_din_elec = int(user[0][2])
                    sign = 1

                    if prev_din_elec != 0:
                        sign = prev_din_elec / abs(prev_din_elec)
                        final_elec_time = prev_din_elec - sign * penalty_time

                    if abs(final_elec_time) > 25:
                        final_elec_time = sign * 25

                    if sign * final_elec_time < 0:
                        final_elec_time = 0

                    # elec_time = datetime.timedelta(minutes=int(user[0][2]))
                    # cfg.dinner_time -= elec_time
                    final_elec_time = datetime.timedelta(minutes=final_elec_time)
                    cfg.dinner_time -= final_elec_time
                    bot.reply_to(message, cfg.revote_msg + additional_msg + str(cfg.dinner_time)[:-3])

                cfg.show_din_time = str(cfg.dinner_time)[:-3]
                print('Время обеда', cfg.show_din_time)
                db.sql_exec(db.upd_election_elec_text, [din_elec, cid, user_id])

        # # понеделбник - денб без мягкого знака
        # ТОЛЬКО ДЛЯ ТЕСТИРОВАНИЯ!!!
        # if tp.soft_sign(message.text) is True:
        if week_day == 0 and hour_msg < 12 and tp.soft_sign(message.text) is True:
            print('##########', datetime.datetime.now(), 'soft_sign')

            bot.reply_to(message, 'ШТРАФ')
            db.sql_exec(db.upd_election_penalty_B_text, [cid, user_id])
            print('ШТРАФ')

        print('##########', datetime.datetime.now(), '\n')


print('here')
bot.remove_webhook()
telegram_polling()
print('here again')
