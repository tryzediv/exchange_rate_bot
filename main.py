import telebot
from config import TOKEN
from currency import keys
from extensions import ConvertionException, CurrencyConverter


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
    try:
        # Получаем переменные из сообщения
        values = message.text.split(' ')
        # Проверяем, что введено верное количество переменных
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров, пример для ввода: доллар рубль 100')
        # Составляем список переменных, избавляемся от реестро-зависимости
        quote, base, amount = list(map(lambda x: x.capitalize(), values))
        # Получаем результат и необходимые для сообщения переменные
        result, text, quote_ticker, base_ticker = CurrencyConverter.get_price(quote, base, amount)
    # Обработка ошибок пользователя
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Упс, вы ошиблись =(\n{e}')
    # Обработка ошибок сервера
    except Exception as e:
        bot.send_message(message.chat.id, f'Со мной что-то не так =(\n{e}')
    else:
        bot.send_message(message.chat.id, f'За 1 {quote} вы можете купить {text} {base}'
                                          f'\nИтого {amount} {quote_ticker} = {result} {base_ticker}')


bot.polling(none_stop=True)
