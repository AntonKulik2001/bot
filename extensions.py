import requests
import json
from config import keys

class ConvertionException(Exception): #класс ошибок
    pass

class ValueConverter: #класс конвертации со статистическим методом и отловом ошибок
    @staticmethod
    def get_price(quote = str, base = str, amount = str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f"https://v6.exchangerate-api.com/v6/4b9bc3205384173849d1eb2b/pair/{quote_ticker}/{base_ticker}/{amount}")
        total = json.loads(r.content)['conversion_result']

        return total

