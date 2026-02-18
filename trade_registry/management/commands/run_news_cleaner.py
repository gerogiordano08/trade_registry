from django.core.management.base import BaseCommand
from trade_registry.services.news_scraper import fetch_ticker_news
from trade_registry.models import News, Ticker
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Executes news cleaner, removes old news from DB.'

    def handle(self, *args, **options):
        now = timezone.now()
        maxtime = timedelta(days=7)
        limit_date = now - maxtime
        deleted_count, _ = News.objects.filter(created_at__lt=limit_date).delete()
        self.stdout.write(self.style.SUCCESS(f"Old news cleaned! [{deleted_count}]"))