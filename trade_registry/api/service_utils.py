import requests
import finnhub
import os
import yfinance as yf
from django.core.cache import cache

def search_alpha(query):
        api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()
        matches = data.get('bestMatches', [])
        #Normalize keys before serializing.---
        clean_matches = []
        for item in matches:
            clean_matches.append({
                'symbol': item.get('1. symbol'),
                'name': item.get('2. name'),
                'market': item.get('4. region')
            })
        return clean_matches

def search_yahoo(query):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}"
        r = requests.get(url, headers=headers, timeout=5)
        data = r.json()        
        matches = data.get('quotes', [])
                
        clean_matches = []
        for item in matches:
            clean_matches.append({
                'symbol': item.get('symbol'),
                'name': item.get('shortname') or item.get('longname')
            })
        return clean_matches

def search_finnhub(query):
        api_key_var = os.environ.get('FINNHUB_API_KEY')
        finnhub_client = finnhub.Client(api_key=api_key_var)
        data = finnhub_client.symbol_lookup(query)
        matches = data.get('result', [])
        #Normalize keys before serializing.---
        clean_matches = []
        for item in matches:
            clean_matches.append({
                'symbol': item.get('symbol'),
                'name': item.get('description'),
            })
        return clean_matches


def get_price(ticker):
    cache_key = f"price_{ticker}"
    price = cache.get(cache_key)
    
    if price is None:
        data = yf.Ticker(ticker)
        price = data.fast_info['last_price']
        cache.set(cache_key, price, 240)
    return price

def get_live_prices_bulk(ticker_list):
    if not ticker_list:
        return {}

    prices = {}
    needed_tickers = []
    for t in ticker_list:
        cached = cache.get(f"price_{t}")
        if cached:
            prices[t] = cached
        else:
            needed_tickers.append(t)

    if needed_tickers:
        data = yf.download(
            tickers=needed_tickers, 
            period="1d", 
            interval="1m", 
            group_by='ticker', 
            auto_adjust=True, 
            threads=True
        )

        for ticker in needed_tickers:
            try:
                last_price = data[ticker]['Close'].iloc[-1] # type: ignore
                prices[ticker] = float(last_price)
                cache.set(f"price_{ticker}", prices[ticker], 120) 
            except Exception:
                prices[ticker] = None 

    return prices