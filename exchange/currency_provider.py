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


if __name__ == "__main__":
    mono_usd = MonoProvider("USD", "UAH")
    mono_eur = MonoProvider("EUR", "UAH")

    privat_usd = PrivatProvider("USD", "UAH")
    privat_eur = PrivatProvider("EUR", "UAH")

    nbu_usd = NBUProvider("USD", "UAH")
    nbu_eur = NBUProvider("EUR", "UAH")

    vkurse_usd = VkurseProvider("USD", "UAH")
    vkurse_eur = VkurseProvider("EUR", "UAH")

    print(f"{mono_usd.name}: {mono_usd.currency_from} to {mono_usd.currency_to} = {mono_usd.get_rate()}")
    print(f"{mono_eur.name}: {mono_eur.currency_from} to {mono_eur.currency_to} = {mono_eur.get_rate()}")
    print()
    print(f"{privat_usd.name}: {privat_usd.currency_from} to {privat_usd.currency_to} = {privat_usd.get_rate()}")
    print(f"{privat_eur.name}: {privat_eur.currency_from} to {privat_eur.currency_to} = {privat_eur.get_rate()}")
    print()
    print(f"{nbu_usd.name}: {nbu_usd.currency_from} to {nbu_usd.currency_to} = {nbu_usd.get_rate()}")
    print(f"{nbu_eur.name}: {nbu_eur.currency_from} to {nbu_eur.currency_to} = {nbu_eur.get_rate()}")
    print()
    print(f"{vkurse_usd.name}: {vkurse_usd.currency_from} to {vkurse_usd.currency_to} = {vkurse_usd.get_rate()}")
    print(f"{vkurse_eur.name}: {vkurse_eur.currency_from} to {vkurse_eur.currency_to} = {vkurse_eur.get_rate()}")
