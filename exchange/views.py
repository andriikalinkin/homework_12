from django.http import JsonResponse
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
