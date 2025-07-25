from methods import *
from datetime import date
class Trade:
    def __init__(self, stock_name:str, quantity:int, buy_date:date, buy_price:float, sell_date, sell_price, user_id:int, profit:float, ended:bool, trade_id:int):
        self.__trade_id__ = trade_id
        self.__stock_name__ = stock_name
        self.__quantity__ = quantity
        self.__buy_date__ = buy_date
        self.__buy_price__ = buy_price
        self.__sell_date__ = sell_date
        self.__sell_price__ = sell_price
        self.__ended__ = ended
        self.__profit__ = profit
        self.__user_id__ = user_id
    def store_trade(self, filename='trades.json'):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        entry = {self.get_trade_id(): {'stock_name':self.get_stock_name(), 'quantity':self.get_quantity(), 'buy_date':self.get_buy_date().strftime('%Y-%m-%d'), 'buy_price':self.get_buy_price(), 'sell_date':self.get_sell_date().strftime('%Y-%m-%d'), 'sell_price':self.get_sell_price(), 'user_id':self.get_user_id(), 'profit':self.get_profit(), 'ended':self.get_ended()}}
        data.update(entry)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    def get_trade_id(self):
        return self.__trade_id__
    def get_stock_name(self):
        return self.__stock_name__
    def get_quantity(self):
        return self.__quantity__
    def get_buy_date(self):
        return self.__buy_date__
    def get_buy_price(self):
        return self.__buy_price__
    def get_sell_date(self):
        return self.__sell_date__
    def get_sell_price(self):
        return self.__sell_price__
    def get_user_id(self):
        return self.__user_id__
    def get_profit(self):
        return self.__profit__
    def get_ended(self):
        return self.__ended__
    