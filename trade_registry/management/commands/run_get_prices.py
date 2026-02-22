from trade_registry.services.utils import get_live_prices_bulk
from trade_registry.models import Ticker
from django.core.management.base import BaseCommand
import math

class Command(BaseCommand):
    help = 'Executes price getter and saves last_price to DB.'
    def handle(self, *args, **options):
        tickers = Ticker.objects.all()
        ticker_set = set(ticker.symbol for ticker in tickers)
        live_prices = get_live_prices_bulk(ticker_set)
        if live_prices:
            for ticker in tickers:
                price = live_prices[ticker.symbol]
                if price is not None and not math.isnan(float(price)):
                    ticker.last_price = live_prices[ticker.symbol]
                else:
                    print(f"{ticker.symbol} could not be fetched (see: get_live_prices_bulk() in utils module)")
        else:
            print("Error fetching live prices.")   
        Ticker.objects.bulk_update(tickers, ['last_price'])
        self.stdout.write(self.style.SUCCESS("Prices synced!"))