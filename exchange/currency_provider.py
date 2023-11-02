from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests


@dataclass
class BuySell:
    buy: float
    sell: float


class BaseProvider(ABC):
    def __init__(self, currency_from: str, currency_to: str,  name: str = None):
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.name = name or "BaseProvider"

    @abstractmethod
    def get_rate(self) -> BuySell:
        pass


class MonoProvider(BaseProvider):
    def __init__(self, currency_from: str, currency_to: str, name: str = None):
        super().__init__(currency_from, currency_to, name or "Monobank")

    iso_codes = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    def get_rate(self) -> BuySell:
        url = "https://api.monobank.ua/bank/currency"
        response = requests.get(url)
        response.raise_for_status()
        currency_from_code = self.iso_codes[self.currency_from]
        currency_to_code = self.iso_codes[self.currency_to]

        for currency in response.json():
            if currency["currencyCodeA"] == currency_from_code and currency["currencyCodeB"] == currency_to_code:
                value = BuySell(float(currency["rateBuy"]), float(currency["rateSell"]))
                return value


class PrivatProvider(BaseProvider):
    def __init__(self, currency_from: str, currency_to: str, name: str = None):
        super().__init__(currency_from, currency_to, name or "Privatbank")

    def get_rate(self) -> BuySell:
        url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"
        response = requests.get(url)
        response.raise_for_status()

        for currency in response.json():
            if currency["ccy"] == self.currency_from and currency["base_ccy"] == self.currency_to:
                value = BuySell(float(currency["buy"]), float(currency["sale"]))
                return value


if __name__ == "__main__":
    provider1 = MonoProvider("USD", "UAH")
    provider3 = PrivatProvider("USD", "UAH")

    print(f"Mono {provider1.currency_from} to {provider1.currency_to} = {provider1.get_rate()}")
    print(f"Privat {provider3.currency_from} to {provider3.currency_to} = {provider3.get_rate()}")
