import requests

from django.apps import AppConfig
from django.conf import settings

from apollo.api import timer


class ApiConfig(AppConfig):
    name = 'apollo.api'

    def __init__(self, app_name, app_module):
        super(ApiConfig, self).__init__(app_name, app_module)

        self.loaded = False
        self.spam_prevention = None
        self.exchange_rates = None

    def ready(self):
        if not self.loaded:
            timer.RepeatedTimer(15, self.fetch_exchange_rates)
            self.fetch_exchange_rates()

    def fetch_exchange_rates(self):
        api_response = requests.post(f'https://min-api.cryptocompare.com/data/pricemulti?fsyms={settings.CRYPTOCOMPARE_TAGS}&tsyms=USD&api_key=' + settings.CRYPTOCOMPARE_API_KEY)
        if api_response.status_code != 200:
            print(f'got status {api_response.status_code}')
            pass

        api_data = api_response.json()

        if self.exchange_rates is None:
            self.exchange_rates = {}

        for crypto_tag in api_data.keys():
            self.exchange_rates[crypto_tag] = api_data[crypto_tag]['USD']
        
        # print('exchange rates:')
        # print(self.exchange_rates)
