from http.client import responses

import telebot
import requests
import datetime as dt


TOKEN = "7620483217:AAHeIYSRxlNxNpsn9i0rt8ffcGzm_lanftE"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, "Вкажіть адресу гаманця(TRC-20) 😎:")

@bot.message_handler(func=lambda message: True)
def get_deposit(message):
    account_id = message.text
    try:
        url = f"https://api.trongrid.io/v1/accounts/{account_id}/transactions/trc20"
        r = requests.get(
            url,
            params={
                'only_to': True,
                # 'only_from': True,
                # 'max_timestamp': dt.datetime.timestamp(dt.datetime.now() - dt.timedelta(hours=6))*1000,
                'only_confirmed': True,
                'limit': 10,
            },
            headers={"accept": "application/json"}
        )
        data = r.json()
        if 'error' in data:
            bot.send_message(message.chat.id, "Гаманець не знайдено 😢")
            return
        for tr in data.get('data', []):
            tx_id = tr.get('transaction_id')
            symbol = tr.get('token_info', {}).get('symbol')
            fr = tr.get('from')
            # to = tr.get('to')

            v = tr.get('value', '')
            dec = -1 * int(tr.get('token_info', {}).get('decimals', '6'))
            f = float(v[:dec] + '.' + v[dec:])

            time_ = dt.datetime.fromtimestamp(float(tr.get('block_timestamp', '')) / 1000)

            bot.send_message(message.chat.id, f"{time_} | {f:>9.02f} {symbol} | {fr} | {tx_id}")

    except Exception as e:

        bot.send_message(message.chat.id, "Error")


bot.polling(non_stop=True)

