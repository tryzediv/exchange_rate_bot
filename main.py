import telebot
import requests
import json
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
# Словарь с доступными валютами
keys = {'Доллар': 'USD', 'Евро': 'EUR', 'Рубль': 'RUB'}


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
    # Составляем список переменных, избавляемся от реестро-зависимости
    quote, base, amount = list(map(lambda x: x.capitalize(), message.text.split(' ')))
    # Отправлем запрос, подставляя нужные переменные из словаря keys
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?'
                     f'fsym='f'{keys[quote]}&tsyms={keys[base]}')
    text = json.loads(r.content)[keys[base]]
    bot.send_message(message.chat.id, f'За 1 {quote} мы можете купить {text} {base}'
                                      f'\nИтого {amount} {keys[quote]} = {float(amount) * float(text)} {keys[base]}')


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, 'Nice meme XDD')


bot.polling(none_stop=True)
