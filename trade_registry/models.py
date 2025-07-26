from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'trends')
    ticker = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    buy_date = models.DateField()
    buy_price = models.DecimalField(max_digits=15, decimal_places=2)
    sell_date = models.DateField()
    sell_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    ended = models.BooleanField()
    profit = models.DecimalField(max_digits=15, decimal_places=2)