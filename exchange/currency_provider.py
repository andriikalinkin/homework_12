from abc import ABC, abstractmethod
import requests


class BaseProvider(ABC):
    def __init__(self, currency_from: str, currency_to: str):
        self.currency_from = currency_from
        self.currency_to = currency_to

    @abstractmethod
    def get_rate(self):
        raise NotImplementedError("get_rate not implemented")


class MonoProvider(BaseProvider):
    iso_codes = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    def get_rate(self):
        url = "https://api.monobank.ua/bank/currency"
        response = requests.get(url)
        response.raise_for_status()
        currency_from_code = self.iso_codes[self.currency_from]
        currency_to_code = self.iso_codes[self.currency_to]

        for currency in response.json():
            if currency["currencyCodeA"] == currency_from_code and currency["currencyCodeB"] == currency_to_code:
                return currency["rateSell"]


if __name__ == "__main__":
    provider = MonoProvider("USD", "UAH")
    print(provider.get_rate())
