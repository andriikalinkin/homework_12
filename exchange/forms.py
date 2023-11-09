from django import forms


class CalculatorForm(forms.Form):
    CURRENCY_CHOICES = [
        ("USD", "USD"),
        ("EUR", "EUR"),
    ]

    value = forms.DecimalField(label="сумма", min_value=0)
    currency_a = forms.ChoiceField(label="из валюты", choices=CURRENCY_CHOICES)
    currency_b = forms.CharField(
        label="в валюту",
        initial="UAH",
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )
