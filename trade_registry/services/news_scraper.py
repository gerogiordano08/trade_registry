import feedparser
from trade_registry.models import Ticker
from email.utils import parsedate_to_datetime
def fetch_ticker_news(ticker:Ticker) -> list[dict]:
    """
        Requests for a news search to Yahoo Finance using URL.
        Args:
            ticker(str): ticker to get news.
        Returns:
            news_items(list[dict]): best news matches for ticker."""
    rss_url = f"https://finance.yahoo.com/rss/headline?s={ticker.symbol}"
    
    feed = feedparser.parse(rss_url)
    
    news_items = []

    for entry in feed.entries:
        news_data = {
            'title': entry.title,
            'link': entry.link,
            'published': parsedate_to_datetime(entry.published),
            'summary': entry.summary if 'summary' in entry else ""
        }
        news_items.append(news_data)
        
    return news_items

