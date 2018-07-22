# -*- coding: utf-8 -*-
import re

#проверка на мягкий знак в сообщении
def soft_sign(str):
    res = re.match('.*ь.*',str)
    if res == None:
        return False
    else:
        return True

print soft_sign('так сказать')