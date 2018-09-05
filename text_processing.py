# -*- coding: utf-8 -*-
import re


# проверка на мягкий знак в сообщении
def soft_sign(str):
    res = re.match('.*ь.*', str)
    if res is None:
        return False
    else:
        return True


def lol_kek_detector(str):
    res = re.match('.*((л[о|е|у|и|а]+л)|(к[е|и]+к)|((ахах)+|(хаха)+)|(l[o|e|i]+l)|(k[e|i]+k))+.*', str, flags=re.I)
    if res is None:
        return False
    else:
        return True


def dinner_time(str):
    res = re.findall('^[+|-][0-9]{1,2}$', str)
    if res is None:
        return False
    else:
        return res[0]


# print(soft_sign('так сказать'))
# print(lol_kek_detector(' кекес'))
# print(lol_kek_detector('ахахххахахаха'))
# print(lol_kek_detector('а '))
# print(dinner_time('+5'))
