from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

import requests


@dataclass
class BuySell:
    buy: Union[float, None]
    sell: Union[float, None]


class BaseProvider(ABC):
    def __init__(self, currency_from: str, currency_to: str,  name: str = None):
        self.currency_from = currency_from.upper()
        self.currency_to = currency_to.upper()
        self.name = name or "BaseProvider"

    @abstractmethod
    def get_rate(self) -> BuySell:
        pass

    def handle_error(self, error):
        print(f"An error occurred while fetching rates from {self.name}: {error}")

    def fetch_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as error:
            self.handle_error(error)
            return None


class MonoProvider(BaseProvider):
    def __init__(self, currency_from: str, currency_to: str, name: str = None):
        super().__init__(currency_from, currency_to, name or "MonoBank")

    iso_codes = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    def get_rate(self) -> BuySell:
        url = "https://api.monobank.ua/bank/currency"
        response = self.fetch_data(url)

        if response:
            currency_from_code = self.iso_codes[self.currency_from]
            currency_to_code = self.iso_codes[self.currency_to]

            for currency in response.json():
                if currency["currencyCodeA"] == currency_from_code and currency["currencyCodeB"] == currency_to_code:
                    value = BuySell(float(currency["rateBuy"]), float(currency["rateSell"]))
                    return value
        value = BuySell(None, None)
        return value


class PrivatProvider(BaseProvider):
    def __init__(self, currency_from: str, currency_to: str, name: str = None):
        super().__init__(currency_from, currency_to, name or "PrivatBank")

    def get_rate(self) -> BuySell:
        url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"
        response = self.fetch_data(url)

        if response:
            for currency in response.json():
                if currency["ccy"] == self.currency_from and currency["base_ccy"] == self.currency_to:
                    value = BuySell(float(currency["buy"]), float(currency["sale"]))
                    return value
        value = BuySell(None, None)
        return value


class NBUProvider(BaseProvider):
    def __init__(self, currency_from: str, currency_to: str, name: str = None):
        super().__init__(currency_from, currency_to, name or "NationalBankOfUkraine")

    def get_rate(self) -> BuySell:
        url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        response = self.fetch_data(url)

        if response:
            for currency in response.json():
                if currency["cc"] == self.currency_from:
                    value = BuySell(float(currency["rate"]), float(currency["rate"]))
                    return value
        value = BuySell(None, None)
        return value


class VkurseProvider(BaseProvider):
    def __init__(self, currency_from: str, currency_to: str, name: str = None):
        super().__init__(currency_from, currency_to, name or "VkurseDpUa")

    def get_rate(self) -> BuySell:
        url = "https://vkurse.dp.ua/course.json"
        response = self.fetch_data(url)

        if response:
            value = False

            if self.currency_from == "USD":
                value = BuySell(float(response.json()["Dollar"]["buy"]), float(response.json()["Dollar"]["sale"]))
            elif self.currency_from == "EUR":
                value = BuySell(float(response.json()["Euro"]["buy"]), float(response.json()["Euro"]["sale"]))
            return value
        value = BuySell(None, None)
        return value


PROVIDERS = [MonoProvider, PrivatProvider, NBUProvider, VkurseProvider]
