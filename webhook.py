import ssl
from aiohttp import web
import telebot
import serverInfo as si
import config as cfg

import random


@cfg.loglog(command='webhook', type='')
def webhook(bot):
    app = web.Application()

    async def handle(request):
        if request.match_info.get('token') == bot.token:
            request_body_dict = await request.json()
            update = telebot.types.Update.de_json(request_body_dict)
            bot.process_new_updates([update])
            return web.Response()
        else:
            return web.Response(status=403)

    app.router.add_post('/{}/'.format(bot.token), handle)

    @bot.message_handler(commands=['coin'])
    @cfg.loglog(command='coin', type='message')
    def throw_coin(message):
        cid = message.chat.id
        bot.send_message(cid, random.choice(cfg.precomand_text))
        bot.send_message(cid, random.choice(cfg.coin_var))

    bot.remove_webhook()

    bot.set_webhook(url=si.serverFullPath, certificate=open(si.sslCert, 'r'))

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(si.sslCert, si.sslPKey)

    web.run_app(
        app,
        host=si.serverListen,
        port=si.serverPort,
        ssl_context=context,
    )
