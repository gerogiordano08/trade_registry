from methods import *
from datetime import date
class Trade:
    def init(self, buy_date:date, sell_date:date, user_id:int, profit:int, ended:bool, trade_id=generate_id('trades.json')):
        self.__trade_id__ = trade_id
        self.__buy_date__ = buy_date
        self.__sell_date__ = sell_date
        self.__user_id__ = user_id
        self.__profit__ = profit
        self.__ended__ = ended
    def get_trade_id(self):
        return self.__trade_id__
    def get_buy_date(self):
        return self.__buy_date__
    def get_sell_date(self):
        return self.__sell_date__
    def get_user_id(self):
        return self.__user_id__
    def get_profit(self):
        return self.__profit__
    def get_ended(self):
        return self.__ended__
    