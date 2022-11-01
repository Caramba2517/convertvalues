from keys import *
import requests
import json

class ConversionExc(Exception):
    pass

class ConvertatorFull:
    @staticmethod
    def get_price(amount: str, quote: str, base: str):
        if quote == base:
            raise ConversionExc(f'Как ты это сделал?! Там же кнопки.')
        try:
            quote_ticker = key_rate[quote]
        except KeyError:
            raise ConversionExc(f'Нужно выбрать на кнопках. Я это не понял: {quote}\nПопробуй еще раз:\n/doit')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionExc(f'Нужно выбрать на кнопках. Я это не понял: {base}\nПопробуй еще раз:\n/doit')
        try:
            amount = float(amount)
        except ValueError:
            raise ConversionExc(f'Нужно ввести сумму в выбранной валюте'
                                f'или использовать точку, вместо запятой'
                                f'Я это не понял: {amount}\nПопробуй еще раз:\n/doit')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[base_ticker]
        total = amount * total_base
        return total

class ConvertatorRate:
    @staticmethod
    def get_rate(quote: str):
        quote_ticket = key_rate[quote]
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticket}&tsyms=RUB')
        text = json.loads(r.content)['RUB']
        return text




