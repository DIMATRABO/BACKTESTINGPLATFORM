class OpenOrder:
    is_buy:bool
    is_future:bool
    openning_price_high:float
    openning_price_low:float
    openning_amount:float
    leverage: float
    #openning_volume_high
    #openning_volume_low



    def __init__(self , is_buy , is_future, openning_price_high, openning_price_low , openning_amount, leverage):
        self.is_buy = is_buy
        self.is_future = is_future
        self.openning_price_high = openning_price_high
        self.openning_price_low = openning_price_low
        self.openning_amount = openning_amount
        self.leverage = leverage




    def max_above_openning_high(self , state):
        if self.openning_price_high is None:
            return False

        if float(state[2]) >= self.openning_price_high:
            return True
        else:
            return False
        
    def min_below_openning_low(self , state):
        
        if self.openning_price_low is None:
            return False
        
        if float(state[3]) <= self.openning_price_low:
            return True
        else:
            return False
