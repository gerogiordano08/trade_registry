from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
# Create your models here.
class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'trends')
    ticker = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    buy_date = models.DateField()
    buy_price = models.DecimalField(max_digits=15, decimal_places=2)
    sell_date = models.DateField(null=True, blank=True)
    sell_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    @property
    def is_ended(self):
        return self.sell_date is not None and self.sell_price is not None
    @property
    def profit(self):
        return (self.sell_price - self.buy_price) * self.quantity if self.is_ended else None
    @property
    def percentage_profit(self):
        return self.profit /(self.quantity * self.buy_price) * 100 if self.is_ended else None
    @property
    def profit_to_loss(self):
        return self.profit * -1 if self.profit < 0 else self.profit 
    @property
    def percentage_profit_to_loss(self):
        return self.percentage_profit * -1 if self.percentage_profit < 0 else self.percentage_profit
