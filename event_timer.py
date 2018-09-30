import threading as th
import datetime
import config as cfg
import database as db
import random

random.seed(datetime.datetime.now().time().second)


@cfg.loglog(command='call_all', type='bot')
def call_all():
    chatUsers = {}
    for cid in cfg.subscribed_chats:
        users = db.sql_exec(db.sel_all_text, (cid,))
        call_users = 'Эй, @all: '
        for i in users:
            call_users += '@' + str(i[4]) + ' '
        chatUsers[cid] = call_users + '\n'
    return chatUsers


@cfg.loglog(command='send_msg', type='bot')
def send_msg(bot, msg, cid=None):
    if cid is None:
        for chat_id in cfg.subscribed_chats:
            bot.send_message(chat_id, msg)
    else:
        bot.send_message(cid, msg)


# @cfg.loglog(command='err_timer', type='bot')
# def err_timer(bot):
#     print('Error with dinner timer!!')
#     timer = th.Timer(60 * 60, one_hour_timer, args=(bot,))
#     timer.start()

#     send_msg(bot, 'Ошибка вычисления таймера, проверь меня!')


@cfg.loglog(command='one_hour_timer', type='bot')
def one_hour_timer(bot):
    time_now = datetime.datetime.now()

    # флаг, который говорит, показывать ли сообщения (показывает, когда 1)
    to_show = 0

    # начальное время таймера (60 * 60)
    timer_time = 3600

    if str(time_now.time().minute) in ('0'):
        to_show = 1
        if str(time_now.time().second) <= '30':
            # нормальная работа
            timer = th.Timer(timer_time, one_hour_timer, args=(bot,))
        else:
            # случай для возможного увеличения времени из-за расчётов программы
            timer_time -= 29
            timer = th.Timer(timer_time, one_hour_timer, args=(bot,))
    else:
        # рандомное время, например, при запуске бота
        # высчитываем время до ближайшего часа **:00:01
        common_time = datetime.timedelta(minutes=60, seconds=0)
        cur_time = datetime.timedelta(minutes=time_now.time().minute, seconds=time_now.time().second)

        delta = common_time - cur_time

        timer_time = int(delta.total_seconds()) + 1

        timer = th.Timer(timer_time, one_hour_timer, args=(bot,))

    print('Секунды до таймера =', timer_time)
    print('Время до таймера =', delta)

    timer.start()

    if to_show == 1:
        # будние дни
        if time_now.weekday() not in (5, 6):
            # доброе утро
            if str(time_now.time().hour) == '9':
                send_msg(bot, random.choice(cfg.gm_text))

            # обед
            if str(time_now.time().hour) == '12':
                chatUsers = call_all()
                for cid, msg in chatUsers.items():
                    send_msg(bot, msg + random.choice(cfg.dinner_text) + cfg.show_din_time, cid)
                    # сохраняем историю голосования
                    db.sql_exec(db.colect_election_hist_text, [str(time_now.date())])
                    # обнуляем время голосования
                    db.sql_exec(db.reset_election_time_text, [0])

            # намёк покушать
            if str(time_now.time().hour) == '17':
                send_msg(bot, random.choice(cfg.eat_text))

            # пора уходить с работы
            if str(time_now.time().hour) == '19':
                send_msg(bot, random.choice(cfg.bb_text))

            # раз в час намекать на попить
            if str(time_now.time().hour) >= '10' and str(time_now.time().hour) <= '18':
                send_msg(bot, random.choice(cfg.pitb_text))
        # выходные
        elif time_now.weekday() == 6:
            # напоминать про дсс
            if str(time_now.time().hour) == '19':
                chatUsers = call_all()
                for cid, msg in chatUsers.items():
                    send_msg(bot, msg + random.choice(cfg.dss_text), cid)

    # выводим дату для лога
    if str(time_now.time().hour) == '0':
        print('New day!', time_now)


# def dinner_time_timer(bot):
#     time_now = datetime.datetime.now()

#     # флаг, который говорит, показывать ли время (показывает, когда 1)
#     to_show = 0

#     # начальное время таймера (24 * 60 * 60)
#     timer_time = 84400

#     # если выводит ошибку, значит не заходит ни в одно время
#     timer = th.Timer(timer_time, err_timer, args=(bot,))

#     # if str(time_now.time())[:8] >= '22:08:00' and str(time_now.time())[:8] <= '22:09:00':
#     if str(time_now.time())[:8] >= '12:00:00' and str(time_now.time())[:8] <= '12:01:00':
#         if time_now.weekday() not in (5, 6):
#             to_show = 1
#             # будние дни
#             if str(time_now.time())[6:8] <= '30':
#                 # нормальная работа
#                 # print('Я работаю нормально!!')
#                 timer = th.Timer(timer_time, dinner_time_timer, args=(bot,))
#             else:
#                 # случай для возможного увеличения времени из-за расчётов программы
#                 timer_time -= 29
#                 timer = th.Timer(timer_time, dinner_time_timer, args=(bot,))
#         else:
#             # выходные, увеличиваем сразу на 2 дня, если суббота
#             # и на 1 день, если воскресенье
#             timer_time *= (7 - time_now.weekday())
#             timer = th.Timer(timer_time, dinner_time_timer, args=(bot,))
#     else:
#         # рандомное время, например, при запуске бота
#         # высчитываем время до 12:00:01
#         # common_time = datetime.timedelta(hours=22, minutes=8, seconds=0)
#         common_time = datetime.timedelta(hours=12, minutes=0, seconds=0)
#         cur_time = datetime.timedelta(hours=time_now.time().hour,
#             minutes=time_now.time().minute, seconds=time_now.time().second)
#         full_day = datetime.timedelta(hours=24, minutes=0, seconds=0)

#         delta = datetime.timedelta()
#         if cur_time > common_time:
#             delta = full_day - cur_time + common_time
#         else:
#             delta = common_time - cur_time

#         timer_time = int(delta.total_seconds()) + 1

#         timer = th.Timer(timer_time, dinner_time_timer, args=(bot,))

#     timer.start()

#     # print(time_now.date())
#     # print(cur_time, common_time, delta)
#     print(timer_time)
#     # print(cfg.show_din_time)

#     if to_show == 1:
#         bot.send_message(cfg.dds_chat_id, call_all() + 'Время обеда: ' + cfg.show_din_time)

#         # сохраняем историю голосования
#         db.sql_exec(db.colect_election_hist_text, [str(time_now.date())])
#         # обнуляем время голосования
#         db.sql_exec(db.reset_election_time_text, [0])
