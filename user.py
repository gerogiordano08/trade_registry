from methods import generate_id
import json
class User:
    def __init__(self, name:str, username:str, winning_trades:list, losing_trades:list, user_id):
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
    def store_user(self, filename='user_ids.json'):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        entry = {self.get_user_id(): self.get_username()}
        data.update(entry)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)