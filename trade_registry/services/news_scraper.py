import feedparser
from email.utils import parsedate_to_datetime
def fetch_ticker_news(symbol):
    
    rss_url = f"https://finance.yahoo.com/rss/headline?s={symbol}"
    
    feed = feedparser.parse(rss_url)
    
    news_items = []
    for _x in range(5):
        for entry in feed.entries:
            news_data = {
                'title': entry.title,
                'link': entry.link,
                'published': parsedate_to_datetime(entry.published),
                'summary': entry.summary if 'summary' in entry else ""
            }
            news_items.append(news_data)
        
    return news_items

