# -*- coding: utf-8 -*-

# токен бота вынесен в отдельный файл,
# чтобы не выкладывать его в открытый доступ
import tokenBot
import datetime

# токен бота
token = tokenBot.token

# приветственное сообщение бота
hello_msg = '''Привет! Я бот для чата DDS. Если тебе это ничего не говорит, иди своей дорогой дальше.
Пока что я умею не очень много чего, но буду расти:
/chto_v_mumu - сегодняшнее меню в МУМУ
/all - пингануть всех в чате
/coin - подбросить монетку
/dice - подбросить кубик
/ball - магический шар
/subscribe - подписаться на рассылку @all
/unsubscribe - отписаться от рассылки @all
/admin_subscribe_for_messages - подписать чат на чтение сообщений
/admin_unsubscribe_for_messages - отписать чат от чтения сообщений
'''

# название базы данных пользователей в чатах
db_name = 'bot_database.db'

# сообщение о подписке на бота человеком
subscribe_msg = '''Принято! Ты подписан на рассылку /all
и теперь можешь голосвать за время обеда.
ВНИМАНИЕ! Бот собирает статистику голосования, если тебе это не нравится,
то ты можешь отписаться командой /unsubscribe в любое время.'''

# сообщение об отписке от бота человеком
unsubscribe_msg = '''Принято! Ты отписан от рассылки /all
и теперь не можешь голосовать за время обеда.'''

# сообщение о повтороной подписке человеком
err_subscribe_msg = '''Ты уже подписан! Ты можешь отписаться командой /unsubscribe в любое время.'''

# сообщение о подписке на бота чатом
subscribe_msg_chatId = '''Принято! Бот читает ваши сообщения:)
Теперь в вашем чате можно голосовать за время обеда и получать различные напоминания.'''

# сообщение об отписке от бота чатом
unsubscribe_msg_chatId = '''Принято! Бот больше не читает ваши сообщения:(
Теперь в вашем чате нельзя голосовать за время обеда и получать различные напоминания.'''

# сообщение о повтороной подписке чатом
err_subscribe_msg_chatId = '''Ваш чат уже подписан!
Вы можете отписаться командой /admin_unsubscribe_for_messages в любое время.'''

# сообщение при голосовании
vote_msg = '''Ты проголосовал! Текущее время '''

# сообщение при переголосовании
revote_msg = '''Ты переголосовал! Текущее время '''

# сообщение об ошибке при голосовании
err_vote_msg = '''Ты не можешь голосовать за время обеда:(
Для этого ты должен подписаться на /all
Ты можешь сделать это командой /subscribe'''

# дефолтное время обеда (часы, минуты)
dinner_default_time = (12, 45)
dinner_max_plusminus_time = 25
dinner_time = 0

# DDS Crew chat_id
dds_chat_id = -282255340

# список чатов, чьи сообщения бот читает
subscribed_chats = []

# список стикеров
sticker_var = ['CAADBAADcAAD-OAEAsKXeIPkd1o3Ag', 'CAADAgADAgADwXKkBLMxNUOXvJrUAg',
               'CAADAgADAQADwXKkBKKoPDv9KrHpAg', 'CAADAgADBwADwXKkBDaH1tzzKIZdAg',
               'CAADAgADAwADwXKkBDjiVNM0pYEPAg']

# прекомандный текст
precomand_text = ['Легко!', 'Пожалуйста!', 'Запросто!', 'Ложись!', 'Лови!', 'Конечно!']

# пекоманды для шара
precomand_ball = ['Трясу шар...', 'Секунду...', 'Сейчас посмотрим...', 'Ща...']

# варианты монетки
coin_var = ['Орёл', 'Решка']

# варианты кубика
dice_var = ['1', '2', '3', '4', '5', '6']

# варианты магического шара
ball_var = ['Бесспорно', 'Предрешено', 'Никаких сомнений', 'Определённо да',
            'Можешь быть уверен в этом', 'Мне кажется — да', 'Вероятнее всего',
            'Хорошие перспективы', 'Знаки говорят — да', 'Да', 'Пока не ясно, попробуй снова',
            'Спроси позже', 'Лучше не рассказывать', 'Сейчас нельзя предсказать',
            'Сконцентрируйся и спроси опять', 'Даже не думай', 'Мой ответ — нет',
            'По моим данным — нет', 'Перспективы не очень хорошие', 'Весьма сомнительно'
            ]

# переменная для показа времени
show_din_time = ''

# текст "доброе утро"
gm_text = ['С добрым утром, работяги!', 'Мир, труд, май!', 'Ммм... Работка!', 'Нада роботац!']

# текст "уходить с работы"
bb_text = ['Пора домой!', 'Работать хорошо, но дома лучше!', 'Пора валить!']

# текст "попить"
pitb_text = ['Может попить? /pitb', 'Просто так напомню, что можно сходить попить... /pitb']

# текст "дсс"
dss_text = ['Завтра DSS, держу в курсе!']

# текст "покушать"
eat_text = ['Вроде как 17:00... Может покушать?', 'Что на счёт покушать?']

# текст "обед"
dinner_text = ['Сегодняшнее время обеда ']

# словарь соответствий номера дня недели и английского/русского названия (для генерации ссылок)
week = {
    0: 'ponedelnik',
    1: 'vtornik',
    2: 'sreda',
    3: 'chetverg',
    4: 'pyatnitsa',
    5: 'subbota',
    6: '-'
}


week_rus = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: '-'
}


# функция преобразования списка подписавшихся чатов,
# для более удобного использования
def subscribed_chats_transform(update):
    subscribed_chats.clear()
    for i in update:
        subscribed_chats.append(i[0])


# логирование команд
def loglog(**command):
    def decorator(func):
        def wrapped(*msg):
            print('##########', datetime.datetime.now(), command['command'])
            # print('### Команда', command['command'])
            if command['type'] == 'message':
                print('Chat_id =', msg[0].chat.id)
                print('User =', msg[0].from_user.id)
            elif command['type'] in ('db_exec', 'db_common'):
                print('Exec text =', msg[0])
                print('Params =', msg[1])
            elif command['type'] == 'sql_chatID':
                print('Chat_id =', msg[0])

            res = func(*msg)
            # print('Конец команды', command['command'])
            print('##########', datetime.datetime.now(), command['command'], '\n')
            return res
        return wrapped
    return decorator
