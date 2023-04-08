from currency import keys
import requests
import json


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # Если в одном сообщении 2 раза введена одинаковая валюта
        if quote == base:
            raise ConvertionException('Пожалуйста вводите разную валюту, '
                                      'пример для ввода: доллар рубль 100')
        # Если первой валюты нет в словаре
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{quote}", '
                                      f'проверьте значения в /values')
        # Если второй валюты нет в словаре
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{base}", '
                                      f'проверьте значения в /values')
        # Если в количество введена не цифра
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество "{amount}", '
                                      f'пример для ввода: доллар рубль 100')

        # Отправляем запрос, подставляя нужные переменные из словаря keys
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?'
                         f'fsym='f'{quote_ticker}&tsyms={base_ticker}')
        # Формируем стоимость за 1 единицу
        text = json.loads(r.content)[keys[base]]
        # Считаем результат
        result = round(float(amount) * float(text), 2)
        return result, text, quote_ticker, base_ticker
