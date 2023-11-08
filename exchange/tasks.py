from datetime import date

from celery import shared_task

from .currency_provider import PROVIDERS
from .models import Rate


CURRENCIES_LIST = [
    "USD",
    "EUR",
]


# @shared_task
def pull_rate():
    for provider_class in PROVIDERS:
        for currency in CURRENCIES_LIST:
            provider = provider_class(currency, "UAH")
            provider_rate = provider.get_rate()

            rate, is_created = Rate.objects.get_or_create(
                vendor=provider.name,
                currency_a=currency,
                currency_b="UAH",
                buy=provider_rate.buy,
                sell=provider_rate.sell,
                date=date.today()
            )

            if is_created:
                print("New rate has been created:", rate)
            else:
                print("The rate is already exists:", rate)
