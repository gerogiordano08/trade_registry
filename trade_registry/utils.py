import yfinance as yf
from django.utils import timezone
from datetime import datetime
def get_price(stock:str):
    ticker = yf.Ticker(stock.upper())
    data = ticker.history(end=timezone.now(), period='7d')
    try:
        return ticker.fast_info['lastPrice']
    except Exception:
        return data.iloc[-1] if not data.empty else None
print(get_price('CRM.BA'))  # Example usage