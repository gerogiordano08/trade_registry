from django_redis import get_redis_connection
import logging
import yfinance as yf
from trade_registry.models import Ticker
import math
logger = logging.getLogger(__name__)

def save_tickers_to_session_pool(session_id, serialized_data, ttl=1800):
    """
    Extracts dictionary tickers and saves them to cache.
    
    Args:
        session_id (str): User session id.
        serialized_data (list): Dictionaries list.
        ttl (int): Time to live.
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
    Atomic verification of ticker in session pool
    Args:
        session_id(str): session id to get ticker pool
        ticker(Ticker): ticker for verification
    """
    if not session_id or not ticker:
        return False
        
    try:
        con = get_redis_connection("default")
        cache_key = f"valid_tickers:{session_id}"
        return con.sismember(cache_key, str(ticker.symbol).upper().strip())
    except Exception:
        return False
    
def get_price(ticker:Ticker) -> float | None:
    """
    Gets live price for a single ticker
    Args:
        ticker(Ticker): ticker to get price.
    Returns:
        price(float): requested price for ticker arg.
        None: in case price couldn't be fetched. Prints message."""
    
    data = yf.Ticker(ticker.symbol)
    price = data.fast_info['last_price']
    if math.isfinite(price):
        return price
    else:
        print(f"Error fetching {ticker.symbol} price")

def get_live_prices_bulk(ticker_list: set[str] | list[str]) -> dict[str, float]:
    """
    Gets live prices for a ticker list
    Optimized to prevent 'NaN' errors
    Args:
        ticker_list(set[str] | list[str]): list or set of saved tickers that require live_price update.
    Returns:
        prices(dict[str, float]): dictionary with key(ticker symbol)(str)-value(last_price)(float) pairs.
        """
    
    if not ticker_list:
        return {}

    prices = {}
    needed_tickers = list(ticker_list)

    if needed_tickers:
        data = yf.download(
            tickers=needed_tickers, 
            period="1d", 
            interval="1m", 
            group_by='ticker', 
            auto_adjust=True, 
            threads=True,
            progress=False
        )

        for ticker in needed_tickers:
            try:
                # (MultiIndex vs SingleIndex)
                ticker_data = data[ticker] if len(needed_tickers) > 1 else data
                
                if not ticker_data.empty:
                    # Drops NaNs from data
                    valid_prices = ticker_data['Close'].dropna()
                    
                    if not valid_prices.empty:
                        last_price = float(valid_prices.iloc[-1])
                        
                        # Checks if infinite or NaN
                        if math.isfinite(last_price):
                            prices[ticker] = last_price
                        else:
                            print(f"DEBUG: {ticker} returned NaN or infinite value.")
                            prices[ticker] = None
                    else:
                        print(f"DEBUG: {ticker} does not have valid prices in set interval.")
                        prices[ticker] = None
                else:
                    print(f"DEBUG: {ticker} returned empty DataFrame.")
                    prices[ticker] = None
                    
            except Exception as e:
                print(f"DEBUG: Error processing {ticker}: {str(e)}")
                prices[ticker] = None

    # Avoids unexisting key error
    for t in ticker_list:
        if t not in prices:
            prices[t] = None

    return prices