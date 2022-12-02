from pycoingecko import CoinGeckoAPI
import telebot
from time import sleep
import schedule
from threading import Thread


bot = telebot.TeleBot("Bot ID", parse_mode=None)
cg = CoinGeckoAPI()

# список морет которые отслеживаем<------------
dict1 = ['ariva', 'axel', 'berry', 'bitcci-cash', 'bitcoinz', 'edain', 'equilibrium', 'amber',
         'empire-token', 'fio-protocol', 'gas', 'gulfcoin-2', 'hoge-finance', 'hzm-coin',
         'intexcoin', 'kala', 'kleekai', 'metaverse-face', 'malinka', 'merchant-token', 'nuco-cloud',
         'ovato', 'plc-ultima', 'pointpay', 'soloxcoin', 'safemoon-inu', 'taboo-token',
         'tcgcoin-2-0', 'the-last-war', 'united-token', 'vica-token', 'volt-inu-2', 'wingriders', 'xrdoge',
         'mirai-token']


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


# функция которая проверяет каждый час на сколько просела или выросла монета<------------
def monday():
    for i in dict1:
        h = cg.get_coins_markets(vs_currency='usd', ids=i, price_change_percentage='1h,24h,7d', sparkline=True)
        name = h[0]['symbol']
        change1h = h[0]['price_change_percentage_1h_in_currency']
        if change1h is None:
            change1h = 0
        if change1h >= 5 or change1h <= -5:
            bot.send_message(Userid, f'{name} change to {round(change1h, 2)}!')


# отправляет цену в телегу<------------
def cheker():
    dictcoin = []
    for i in dict1:
        h = cg.get_coins_markets(vs_currency='usd', ids=i, price_change_percentage='1h,24h,7d', sparkline=True)
        name = h[0]['symbol']
        correntprice = h[0]['current_price']
        dictcoin += name, correntprice
    bot.send_message(Userid, f'{dictcoin}')


# настройка работы функций по времени<------------
schedule.every().hour.do(monday)
schedule.every().day.at("9:30").do(cheker)
schedule.every().day.at("18:30").do(cheker)
Thread(target=schedule_checker).start()
bot.infinity_polling()
