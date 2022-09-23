
class FuturesOrder:
    is_long:bool
    is_open:bool

    openning_price:float
    openning_amount:float
    leverage: float

    def __init__(self , is_long , is_open , openning_price , openning_amount , leverage ):
        self.is_long=is_long
        self.is_open = is_open
        self.openning_price = openning_price
        self.openning_amount = openning_amount
        self.leverage = leverage



