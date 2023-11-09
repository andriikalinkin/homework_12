from django.urls import path

from . import views

urlpatterns = [
    path("exchange-rates/", views.exchange_rates, name="exchange-rates"),
    path("calculator/", views.calculator, name="calculator"),
]
