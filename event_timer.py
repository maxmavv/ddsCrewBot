import threading as th
import datetime


def err_timer():
    print('Error with dinner timer!!!!')
    timer = th.Timer(24 * 60 * 60, dinner_time)
    timer.start()


def dinner_time():
    time_now = datetime.datetime.now()
    # print(str(time_now.time())[:8])

    # если выводит ошибку, значит не заходит ни в одно время
    timer = th.Timer(24 * 60 * 60, err_timer)

    if str(time_now.time())[:8] >= '12:00:00' and str(time_now.time())[:8] <= '12:01:00':
        if time_now.weekday() not in (5, 6):
            # будние дни
            if str(time_now.time())[6:8] <= '30':
                # нормальная работа
                timer = th.Timer(24 * 60 * 60, dinner_time)
            else:
                # случай для возможного увеличения времени из-за расчётов программы
                timer = th.Timer(24 * 60 * 60 - 29, dinner_time)
        else:
            # выходные, увеличиваем сразу на два дня
            timer = th.Timer(2 * 24 * 60 * 60, dinner_time)
    else:
        # рандомное время, например, при запуске бота
        # высчитываем время до 12:00:01
        common_time = datetime.timedelta(hours=12, minutes=00)
        cur_time = datetime.timedelta(hours=time_now.time().hour, minutes=time_now.time().minute)

        delta = datetime.timedelta()
        if cur_time > common_time:
            delta = cur_time - common_time
        else:
            delta = common_time - cur_time

        timer = th.Timer(int(delta.total_seconds()) + 1, dinner_time)

    timer.start()


dinner_time()
