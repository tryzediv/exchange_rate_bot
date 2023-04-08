import telebot
import requests
import json
from config import TOKEN, keys
from extensions import ConvertionException


bot = telebot.TeleBot(TOKEN)


# Приветственное сообщение
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.username.capitalize()}, '
                                      'чтобы начать работу пришли мне <имя валюты> '
                                      '<в какую валюту перевести> <количество переводимой валюты>'
                                      '\nНапример: доллар рубль 100'
                                      '\nУвидеть список всех доступных валют: /values')


# Команда /value отправляет список всех доступных валют
@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text += f'{key}, '
    # Приводим список доступных валют в читаемый вид
    bot.send_message(message.chat.id, text[:-2])


@bot.message_handler(content_types=['text'])
def convert(message):
    values = message.text.split(' ')

    if len(values) > 3:
        raise ConvertionException('Слишком много параметров,\nпример для ввода: доллар рубль 100')

    # Составляем список переменных, избавляемся от реестро-зависимости
    quote, base, amount = list(map(lambda x: x.capitalize(), values))

    if quote == base:
        raise ConvertionException('Пожалуйста вводите разную валюту,\nпример для ввода: доллар рубль 100')

    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {quote}, проверьте значения в /value')

    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {base}, проверьте значения в /value')
    # Отправлем запрос, подставляя нужные переменные из словаря keys
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?'
                     f'fsym='f'{quote_ticker}&tsyms={base_ticker}')
    text = json.loads(r.content)[keys[base]]
    result = round(float(amount) * float(text), 2)
    bot.send_message(message.chat.id, f'За 1 {quote} вы можете купить {text} {base}'
                                      f'\nИтого {amount} {quote_ticker} = {result} {base_ticker}')


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, 'Nice meme XDD')


bot.polling(none_stop=True)
