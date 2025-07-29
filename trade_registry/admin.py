from django.contrib import admin
from .models import Trade
# Register your models here.
@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticker', 'quantity', 'buy_date', 'buy_price', 'sell_date', 'sell_price')
    list_filter = ('user', 'ticker')
    search_fields = ('ticker', 'user__username')
    date_hierarchy = 'buy_date'
    ordering = ('-buy_date',)