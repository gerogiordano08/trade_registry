from django_redis import get_redis_connection
import logging
import yfinance as yf
from django.core.cache import cache
from trade_registry.models import Ticker

logger = logging.getLogger(__name__)

def save_tickers_to_session_pool(session_id, serialized_data, ttl=1800):
    """
    Extrae los símbolos de una lista de diccionarios y los guarda en Redis.
    
    Args:
        session_id (str): ID de sesión del usuario.
        serialized_data (list): Lista de dicts (ej: resultados de la API).
        ttl (int): Tiempo de vida en segundos.
    """
    if not session_id or not serialized_data:
        return False

    try:
        con = get_redis_connection("default")
        cache_key = f"valid_tickers:{session_id}"
        symbols = [
            str(item['symbol']).upper().strip() 
            for item in serialized_data 
            if isinstance(item, dict) and 'symbol' in item
        ]
        if symbols:
            con.sadd(cache_key, *symbols)
            con.expire(cache_key, ttl)
            return True
            
    except Exception as e:
        logger.error(f"Error processing ticker pool in Redis: {e}")
        return False
        
    return False

def is_ticker_in_session_pool(session_id, ticker:Ticker):
    """
    Verifica de forma atómica si un ticker existe en el pool de la sesión.
    """
    if not session_id or not ticker:
        return False
        
    try:
        con = get_redis_connection("default")
        cache_key = f"valid_tickers:{session_id}"
        return con.sismember(cache_key, str(ticker.symbol).upper().strip())
    except Exception:
        return False
    
def get_price(ticker:Ticker):
    cache_key = f"price_{ticker.symbol}"
    price = cache.get(cache_key)
    
    if price is None:
        data = yf.Ticker(ticker.symbol)
        price = data.fast_info['last_price']
        cache.set(cache_key, price, 240)
    return price

def get_live_prices_bulk(ticker_list:set[str]|list[str]):
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