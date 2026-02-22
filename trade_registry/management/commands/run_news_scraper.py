from django.core.management.base import BaseCommand
from trade_registry.services.news_scraper import fetch_ticker_news
from trade_registry.models import News, Ticker

class Command(BaseCommand):
    help = 'Executes news scraper and saves news to DB.'

    def handle(self, *args, **options):
        for ticker in Ticker.objects.all():
            news = fetch_ticker_news(ticker)
            for n in news:
                news_obj, _created = News.objects.get_or_create(title=n['title'], defaults=n)
                news_obj.tickers.add(ticker)
        self.stdout.write(self.style.SUCCESS("News synced!"))