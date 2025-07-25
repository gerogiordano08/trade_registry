from datetime import date
import json
import yfinance as yf
def get_price(date:str, stock:str):
    ticker = yf.Ticker(stock.upper())
    data = ticker.history(start=date, period='1d')
    return data['Close'].iloc[0] if not data.empty else None

def get_today_date():
    return date.today().strftime('%Y-%m-%d')
def user_exists(username, filename='user_ids.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    usernames = list(data.values())
    return 1 if username in usernames else 0
def check_last_id(filename='user_ids.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    ids= list(data.keys())
    last_id = ids[-1]
    return int(last_id)
def id_exists(id, filename='user_ids.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    ids= list(data.keys())
    return 1 if id in ids else 0
def generate_id(filename='user_ids.json'):
    new_id = check_last_id(filename) + 1
    while id_exists(new_id, filename) == 1:
        new_id += 1
    return new_id
