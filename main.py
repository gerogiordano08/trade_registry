from trade import Trade
from user import User
from methods import *
def main():
    print('Hello, Gerónimo!')
    user_id = 1
    x = 0
    on = True
    while on == True:
        x = int(input('1. Add trade\n2. Check trades\n3. Exit\n'))
        if x == 1:
            stock_name = input('Enter stock name: ').upper()
            quantity = int(input('Enter quantity: '))
            buy_date = input('Enter buy date (YYYY-MM-DD): ')
            buy_date = date.fromisoformat(buy_date)
            buy_price = float(input('Enter buy price: '))
            ended = input('Have you sold the stock? (yes/no): ').strip().lower()
            if ended == 'yes':
                sell_date = input('Enter sell date (YYYY-MM-DD): ')
                sell_date = date.fromisoformat(sell_date)
                sell_price = float(input('Enter sell price: '))
            else:
                sell_date = None
                sell_price = None
            if sell_price is None:
                try:
                    profit = (get_price(get_today_date(), stock_name) - buy_price) * quantity
                except:
                    print(f'Data for {stock_name} not found')
            else:
                profit = (sell_price - buy_price) * quantity
            trade_id = generate_id('trades.json')
            
            trade = Trade(stock_name, quantity, buy_date, buy_price, sell_date, sell_price, user_id, profit, ended == 'yes', trade_id)
            trade.store_trade()
            print(f'Trade added with ID: {trade.get_trade_id()}')

        elif x == 2:
            with open('trades.json', 'r', encoding='utf-8') as f:
                trades = json.load(f)
            for trade_id, trade_info in trades.items():
                print(f'Trade ID: {trade_id}\n-Stock: {trade_info["stock_name"]}\n-Quantity: {trade_info["quantity"]}\n–Buy Date: {trade_info["buy_date"]}\n-Buy Price: {trade_info["buy_price"]}\n-Sell Date: {trade_info["sell_date"]}\n-Sell Price: {trade_info["sell_price"]}\n-Profit: {trade_info["profit"]}\n-Ended: {"Yes" if trade_info["ended"] == True else "No"}')
        elif x == 3:
            print('Exiting...')
            return
if __name__ == '__main__':
    main()

