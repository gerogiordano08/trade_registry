from django.contrib import admin
from .models import Trade, News, Ticker, BlacklistedIP
# Register your models here.
@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticker', 'quantity', 'buy_date', 'buy_price', 'sell_date', 'sell_price')
    list_filter = ('user', 'ticker')
    search_fields = ('ticker', 'user__username')
    date_hierarchy = 'buy_date'
    ordering = ('-buy_date',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'published', 'summary', 'created_at')
    list_filter = ('published', 'tickers')
    search_fields = ('title',)
    date_hierarchy = 'published'
    ordering = ('-published',)

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'last_price')
    search_fields = ('symbol',)

@admin.register(BlacklistedIP)
class BlacklistedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'attempt_count', 'reason', 'first_attempt', 'last_attempt')
    list_filter = ('first_attempt', 'last_attempt')
    search_fields = ('ip_address', 'reason')
    date_hierarchy = 'last_attempt'
    ordering = ('-last_attempt',)
    actions = ['remove_blacklist']
    
    def remove_blacklist(self, request, queryset):
        queryset.delete()
        self.message_user(request, "Selected IPs have been removed from blacklist.")
    remove_blacklist.short_description = "Remove selected IPs from blacklist"

