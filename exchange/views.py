from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from .forms import CalculatorForm
from .models import Rate


# Create your views here.
def exchange_rates(request):
    response_data = {
        "current_rates": [
            {
                "id": rate.id,
                "data": rate.date,
                "vendor": rate.vendor,
                "currency_a": rate.currency_a,
                "currency_b": rate.currency_b,
                "sell": rate.sell,
                "buy": rate.buy,
            }
            for rate in Rate.objects.all()
        ]
    }
    return JsonResponse(response_data)


def calculator(request):
    if request.method == "POST":
        form = CalculatorForm(request.POST)

        if form.is_valid():
            value = form.cleaned_data["value"]
            currency_a = form.cleaned_data["currency_a"]

            best_rate = Rate.objects.filter(
                currency_a=currency_a
            ).order_by("sell").first()

            if best_rate:
                converted_value = value * best_rate.sell
                return HttpResponse(f"{value} {currency_a} = {round(converted_value, 2)} UAH")

    form = CalculatorForm
    return render(request, "calculator.html", {"form": form})
