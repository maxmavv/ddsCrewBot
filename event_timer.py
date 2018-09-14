import threading as th
import datetime
import config as cfg
import database as db


def err_timer(bot):
    print('Error with dinner timer!!')
    timer = th.Timer(24 * 60 * 60, dinner_time_timer, args=(bot,))
    timer.start()

    bot.send_message(cfg.dds_chat_id, 'Ошибка вычисления таймера, проверь меня!')


def dinner_time_timer(bot):
    time_now = datetime.datetime.now()

    # флаг, который говорит, показывать ли время (показывает, когда 1)
    to_show = 0

    # начальное время таймера (24 * 60 * 60)
    timer_time = 84400

    # если выводит ошибку, значит не заходит ни в одно время
    timer = th.Timer(timer_time, err_timer, args=(bot,))

    # if str(time_now.time())[:8] >= '22:08:00' and str(time_now.time())[:8] <= '22:09:00':
    if str(time_now.time())[:8] >= '12:00:00' and str(time_now.time())[:8] <= '12:01:00':
        if time_now.weekday() not in (5, 6):
            to_show = 1
            # будние дни
            if str(time_now.time())[6:8] <= '30':
                # нормальная работа
                print('Я работаю нормально!!')
                timer = th.Timer(timer_time, dinner_time_timer, args=(bot,))
            else:
                # случай для возможного увеличения времени из-за расчётов программы
                timer_time -= 29
                timer = th.Timer(timer_time, dinner_time_timer, args=(bot,))
        else:
            # выходные, увеличиваем сразу на 2 дня, если суббота
            # и на 1 день, если воскресенье
            timer_time *= (7 - time_now.weekday())
            timer = th.Timer(timer_time, dinner_time_timer, args=(bot,))
    else:
        # рандомное время, например, при запуске бота
        # высчитываем время до 12:00:01
        # common_time = datetime.timedelta(hours=22, minutes=8, seconds=0)
        common_time = datetime.timedelta(hours=12, minutes=0, seconds=0)
        cur_time = datetime.timedelta(hours=time_now.time().hour,
            minutes=time_now.time().minute, seconds=time_now.time().second)
        full_day = datetime.timedelta(hours=24, minutes=0, seconds=0)

        delta = datetime.timedelta()
        if cur_time > common_time:
            delta = full_day - cur_time + common_time
        else:
            delta = common_time - cur_time

        timer_time = int(delta.total_seconds()) + 1

        timer = th.Timer(timer_time, dinner_time_timer, args=(bot,))

    timer.start()

    # print(str(time_now.time()))
    print(cur_time, common_time, delta)
    print(timer_time)
    print(cfg.show_din_time)

    if to_show == 1:
        bot.send_message(cfg.dds_chat_id, 'Время обеда: ' + cfg.show_din_time)

        # обнуляем время голосования
        db.sql_exec(db.reset_election_time_text, (0))
