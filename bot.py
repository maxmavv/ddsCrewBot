# -*- coding: utf-8 -*-
import config as cfg
import text_processing as tp
import mumu
import telebot
import time
import datetime
import database as db

bot = telebot.TeleBot(cfg.token, threaded=False)

week_day = datetime.datetime.today().weekday()

#стучимся к серверам ТГ, если не пускает
def telegram_polling():
    try:
        bot.polling(none_stop=True, timeout=60) #constantly get messages from Telegram
        print 'ok'
    except Exception as e:
        #print e
        bot.stop_polling()
        time.sleep(10)
        print 'try...'
        telegram_polling()

#приветствие
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    cid = message.chat.id
    bot.send_message(cid, cfg.hello_msg)

#меню в муму
@bot.message_handler(commands=['chto_v_mumu'])
def send_mumu(message):
    cid = message.chat.id
    #week_day = datetime.datetime.today().weekday()
    lunches = mumu.lunches(week_day)

    bot.send_message(cid, lunches[0][0])
    bot.send_message(cid, lunches[0][1])
    bot.send_message(cid, lunches[1][0])
    bot.send_message(cid, lunches[1][1])

#регистрируем человека в списке участников чата по его запросу
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    cid = message.chat.id
    user = message.from_user
    db.insert_into_table(cid, user)
    bot.send_message(cid, cfg.subscribe_msg)

#удаляем человека из списка участников чата по его запросу
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    cid = message.chat.id
    user_id = message.from_user.id
    db.delete_from_table(cid, user_id)
    bot.send_message(cid, cfg.unsubscribe_msg)

#призвать всех
@bot.message_handler(commands=['all'])
def ping_all(message):
    cid = message.chat.id
    user_id = message.from_user.id
    users = db.select_from_table(cid)
    call_text = 'Эй, @all: '
    #бежим по всем юзерам в чате
    print 'users:', users
    for i in users:
        print i
        print i[1]
        print i[4]
        print user_id
        #если юзер не тот, кто вызывал all, уведомляем его
        if i[1]<>user_id:
            call_text = call_text +' @' +str(i[4])
        print call_text
    msg = message.text.encode("utf-8")[4:]
    bot.send_message(cid, call_text + msg)

print 'here'
telegram_polling()
print 'here again'

#понедельник - день без мягкого знака
@bot.message_handler(func=lambda message: tp.soft_sign(message.text.encode("utf-8")) == True)
def soft_sign_warning(message):
    #print '_ь_', week_day
    #print message.text.encode("utf-8")
    if week_day == 0:
        bot.reply_to(message, 'ШТРАФ')

#@bot.py.message_handler(content_types=["text"])
#def repeat_all_messages(message):
    #bot.py.send_message(message.chat.id, message.text)
#    bot.py.send_message(message.chat.id, 'Привет!')
