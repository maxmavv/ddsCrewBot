# -*- coding: utf-8 -*-
import config as cfg
import re


# проверка на мягкий знак в сообщении
def soft_sign(msg):
    res = re.match('.*ь.*', msg)
    if res is None:
        return False
    else:
        return True


def lol_kek_detector(msg):
    res = re.match('.*((л[о|е|у|и|а]+л)|(к[е|и]+к)|((ахах)+|(хаха)+)|(l[o|e|i]+l)|(k[e|i]+k))+.*', msg, flags=re.I)
    if res is None:
        return False
    else:
        return True


def dinner_election(msg):
    res = re.findall('^[+|-][0-9]{1,2}$', msg)
    if res == []:
        return False
    else:
        if abs(int(res[0])) <= cfg.dinner_max_plusminus_time:
            return int(res[0])


# print(soft_sign('так сказать'))
# print(lol_kek_detector(' кекес'))
# print(lol_kek_detector('ахахххахахаха'))
# print(lol_kek_detector('а '))
# print(dinner_election('jnkm'))
