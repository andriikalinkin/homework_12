from datetime import date

from django.db.models import Q
from celery import shared_task

from .currency_provider import PROVIDERS
from .models import Rate


# @shared_task
def pull_rate():
    for provider_class in PROVIDERS:
        for currency in ["USD", "EUR"]:
            provider = provider_class(currency, "UAH")
            provider_rate = provider.get_rate()

            template = Q(
                vendor=provider.name,
                currency_a=currency,
                currency_b="UAH",
                buy=provider_rate.buy,
                sell=provider_rate.sell,
                date=date.today(),
            )

            rate, created = Rate.objects.get_or_create(
                template,
                defaults={
                    "buy": provider_rate.buy,
                    "sell": provider_rate.sell,
                }
            )

            if created:
                print("New rate has been created:", rate)
            else:
                print("The rate is already exists:", rate)
