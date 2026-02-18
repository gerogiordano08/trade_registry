from trade_registry.services.utils import get_live_prices_bulk
from trade_registry.models import Ticker
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Executes news scraper and saves news to DB.'
    def handle(self, *args, **options):
        tickers = Ticker.objects.all()
        ticker_set = set(ticker.symbol for ticker in tickers)
        live_prices = get_live_prices_bulk(ticker_set)
        for ticker in tickers:
            ticker.last_price = live_prices[ticker.symbol]
            
        Ticker.objects.bulk_update(tickers, ['last_price'])
        self.stdout.write(self.style.SUCCESS("Prices synced!"))