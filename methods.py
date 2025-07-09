import yfinance as yf
import pandas
from datetime import date
def get_price(date:str, stock:str):
    ticker = yf.Ticker(stock.upper())
    data = ticker.history(start=date, period='1d')
    return data['Close'].iloc[0] if not data.empty else None

def get_today_date():
    return date.today().strftime('%Y-%m-%d')
