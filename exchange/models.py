from django.db import models


# Create your models here.
class Rate(models.Model):
    vendor = models.CharField(max_length=55)
    currency_a = models.CharField(max_length=3)
    currency_b = models.CharField(max_length=3)
    buy = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    sell = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    date = models.DateField()
