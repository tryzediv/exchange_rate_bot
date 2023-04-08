import telebot
import requests
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
# Словарь с доступными валютами
keys = {'USD': 'Доллар', 'EUR': 'Евро', 'RUB': 'Рубль'}


# Приветственное сообщение
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.username.capitalize()}, '
                          f'чтобы начать работу пришли мне <имя валюты> '
                          f'<в какую валюту перевести> <количество переводимой валюты>'
                          f'\nНапример: доллар рубль 100'
                          f'\nУвидеть список всех доступных валют: /values')


# Команда /value отправляет список всех доступных валют
@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты: '
    for key in keys.values():
        text += f'{key}, '
    bot.send_message(message.chat.id, text[:-2])


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, 'Nice meme XDD')


bot.polling(none_stop=True)
