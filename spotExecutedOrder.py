
class SpotExecutedOrder:
    is_buy = bool
    openning_time = float
    openning_price = float
    openning_amount = float
    openning_wallet_worth = float
    breakeaven = float
  
  
    def __init__(self , is_buy ,openning_time , openning_price , openning_amount , openning_wallet_worth , breakeaven):
        self.is_buy = is_buy
        self.openning_time = openning_time
        self.openning_price= openning_price 
        self.openning_amount = openning_amount
        self.openning_wallet_worth = openning_wallet_worth
        self.breakeaven = breakeaven

    def to_string(self):
        return f'    - {"buy" if self.is_buy else "sell"} -- at price { round(self.openning_price,3)} -- amount of {round(self.openning_amount,3)} --wollet worth = {round(self.openning_wallet_worth,3)} --breakeaven at {round(self.breakeaven,3)} '