import requests
import finnhub
import os


def search_alpha(query:str) -> list[dict]:
        """
        Requests for a ticker search to Alpha Vantage API
        Args:
            query(str): search query.
        Returns:
            clean_matches(list[dict]): best matches for search query."""
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
        """
        Requests for a ticker search to Yahoo Finance using url.
        Args:
            query(str): search query.
        Returns:
            clean_matches(list[dict]): best matches for search query."""
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
        """
        Requests for a ticker search to Finnhub API
        Args:
            query(str): search query.
        Returns:
            clean_matches(list[dict]): best matches for search query."""
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


