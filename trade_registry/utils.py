from .models import Ticker

def get_ticker_name(ticker:str) -> str:
    """Returns the official name of a given ticker

    Args:
        ticker (str): Ticker symbol

    Returns:
        str: name of given ticker
    """
    dictionary = {}
    for tick in Ticker.objects.all():
        dictionary[tick.symbol] = tick.name
    return dictionary[ticker]