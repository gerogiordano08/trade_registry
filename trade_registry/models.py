from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from collections import namedtuple
import math
# Create your models here.
TradeMetrics = namedtuple('TradeMetrics', ['live_price', 'live_profit', 'live_percentage_profit', 'is_loss'])

class Ticker(models.Model):
    symbol = models.CharField(unique=True)
    name = models.CharField()
    last_price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
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
        return (self.sell_price - self.buy_price) * self.quantity if self.is_ended else 0 #type:ignore
    @property
    def percentage_profit(self):
        return self.profit /(self.quantity * self.buy_price) * 100 if self.is_ended else 0 #type:ignore
    @property
    def abs_profit(self):
        return abs(self.profit)
    @property
    def abs_percentage_profit(self):
        return abs(self.percentage_profit)
    
    def get_live_metrics(self, price):
        live_profit = (Decimal(price) - self.buy_price) * self.quantity
        live_percentage_profit = abs(((Decimal(price) - self.buy_price) / self.buy_price ) * 100 )
        is_loss = live_profit < 0
        live_profit = abs(live_profit)
        return TradeMetrics(live_price=price, live_profit=live_profit, live_percentage_profit=live_percentage_profit, is_loss=is_loss)

class News(models.Model):
    title = models.CharField()
    link = models.CharField()
    published = models.DateTimeField()
    tickers = models.ManyToManyField(
        Ticker, 
        related_name='news',
        blank=True
    )
    summary = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True, null=True) 
    class Meta:
        ordering = ['-published']
    @property
    def get_delta_time(self) -> str:
        now = timezone.now()
        delta = now - self.published
        total_seconds = int(delta.total_seconds())
        if total_seconds < 60:
            return f"{total_seconds} second{'s' if math.floor(total_seconds) != 1 else ''}"
        if total_seconds < 60*60:
            return f"{math.floor(total_seconds/60)} minute{'s' if math.floor(total_seconds/60) != 1 else ''}" 
        if delta.days < 1:
            return f"{math.floor(total_seconds/(60*60))} hour{'s' if math.floor(total_seconds/(60*60)) != 1 else ''}"
        if delta.days < 365: 
            return f"{delta.days} day{'s' if math.floor(delta.days) != 1 else ''}"
        if delta.days > 365:
            return f"{math.floor(delta.days/365)} year{'s' if math.floor(delta.days/365) != 1 else ''}"
        return "Unknown"

    @property
    def get_age_in_db(self):
        return timezone.now() - self.created_at if self.created_at is not None else timezone.now() - timezone.now()


class BlacklistedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255, blank=True)
    attempt_count = models.PositiveIntegerField(default=1)
    first_attempt = models.DateTimeField(auto_now_add=True)
    last_attempt = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_attempt']
    
    def __str__(self):
        return f"{self.ip_address} ({self.attempt_count} attempts)"