from django import forms

from .models import Rate


class CalculatorForm(forms.Form):
    CURRENCY_CHOICES = [
        ("USD", "USD"),
        ("EUR", "EUR"),
    ]

    value = forms.DecimalField(label="Amount", min_value=0)
    currency_a = forms.ChoiceField(label="Which currency should be converted to UAH", choices=CURRENCY_CHOICES)
    date = forms.DateField(
        label="Select exchange rate date",
        widget=forms.TextInput(attrs={'type': 'date'}),
    )
