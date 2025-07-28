import yfinance as yf
def get_price(date:str, stock:str):
    ticker = yf.Ticker(stock.upper())
    data = ticker.history(end=date, period='7d')
    return data['Close'].iloc[-1] if not data.empty else None
print(get_price('2025-07-27', 'CRM.BA'))  # Example usage