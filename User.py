from methods import *
from trade import Trade
class User:
    def __init__(self, name:str, username:str, winning_trades:list[Trade], losing_trades:list[Trade], user_id=generate_id()):
        self.__name__ = name
        self.__username__ = username
        self.__user_id__ = user_id
        self.__winning_trades__ = winning_trades
        self.__losing_trades__ = losing_trades 
        
    def get_user_id(self):
        return self.__user_id__
    def get_username(self):
        return self.__username__
    def get_name(self):
        return self.__name__
    def get_win_trades(self):
        return self.__winning_trades__
    def get_los_trades(self):
        return self.__losing_trades__
