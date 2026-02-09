from django_redis import get_redis_connection
import logging

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
        logger.error(f"Error procesando pool de tickers en Redis: {e}")
        return False
        
    return False

def is_ticker_in_session_pool(session_id, ticker):
    """
    Verifica de forma atómica si un ticker existe en el pool de la sesión.
    """
    if not session_id or not ticker:
        return False
        
    try:
        con = get_redis_connection("default")
        cache_key = f"valid_tickers:{session_id}"
        return con.sismember(cache_key, str(ticker).upper().strip())
    except Exception:
        return False