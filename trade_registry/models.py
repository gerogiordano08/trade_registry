from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from collections import namedtuple
import math
# Create your models here.
TradeMetrics = namedtuple('TradeMetrics', ['live_price', 'live_profit', 'live_percentage_profit', 'is_loss'])

class Ticker(models.Model):
    symbol = models.CharField()
    name = models.CharField()
    
    def __str__(self) -> str:
        return self.symbol
    
class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'trades')
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name= 'trades')
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
        return (self.sell_price - self.buy_price) * self.quantity if self.is_ended else None #type:ignore
    @property
    def percentage_profit(self):
        return self.profit /(self.quantity * self.buy_price) * 100 if self.is_ended else None #type:ignore
    @property
    def profit_to_loss(self):
        return self.profit * -1 if self.profit < 0 else self.profit #type:ignore
    @property
    def percentage_profit_to_loss(self):
        return self.percentage_profit * -1 if self.percentage_profit < 0 else self.percentage_profit #type:ignore
    def get_live_metrics(self, price):
        live_profit = (Decimal(price) - self.buy_price) * self.quantity
        live_percentage_profit = ((Decimal(price) - self.buy_price) / self.buy_price )* 100 
        is_loss = live_profit < 0
        if live_profit < 0:
            live_profit = live_profit * -1
            live_percentage_profit = live_percentage_profit * -1
        return TradeMetrics(live_price=price, live_profit=live_profit, live_percentage_profit=live_percentage_profit, is_loss=is_loss)

class News(models.Model):
    title = models.CharField()
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name= 'news')
    link = models.CharField()
    published = models.DateTimeField()
    summary = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True, null=True) 
    class Meta:
        ordering = ['-published']
    @property
    def get_delta_time(self) -> str:
        now = timezone.now()
        delta = now - self.published
        if delta.seconds < 60:
            return f"{delta.seconds} second{'s' if math.floor(delta.seconds) != 1 else ''}"
        if delta.seconds < 60*60:
            return f"{math.floor(delta.seconds/60)} minute{'s' if math.floor(delta.seconds/60) != 1 else ''}" 
        if delta.days < 1:
            return f"{math.floor(delta.seconds/(60*60))} hour{'s' if math.floor(delta.seconds/(60*60)) != 1 else ''}"
        if delta.days < 365: 
            return f"{delta.days} day{'s' if math.floor(delta.days) != 1 else ''}"
        if delta.days > 365:
            return f"{math.floor(delta.days/365)} year{'s' if math.floor(delta.days/365) != 1 else ''}"
        return "Unknown"

    @property
    def get_age_in_db(self):
        return timezone.now() - self.created_at if self.created_at is not None else timezone.now() - timezone.now()