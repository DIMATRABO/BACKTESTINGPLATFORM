from hashlib import new
from futuresOrder import FuturesOrder
from typing import List
import random

class Wallet:
    TRADING_PAIR:str
    USDT_DISPO:float
    COIN_DISPO:float
    FUTURES_FREE : float
    FUTURES_IN_OERDER: int
    futures_open_orders = List[FuturesOrder] # Same Trading Pair
 

    def __init__(self, TRADING_PAIR, USDT_DISPO , COIN_DISPO,FUTURES_FREE , SLIPPAGE , FEES):
        self.TRADING_PAIR=TRADING_PAIR
        self.USDT_DISPO = USDT_DISPO
        self.COIN_DISPO = COIN_DISPO
        self.FUTURES_FREE = FUTURES_FREE
        self.FUTURES_IN_OERDER = 0
        self.LIQUIDATION_PRICE = None
        self.futures_open_orders = []

        self.SLIPPAGE = SLIPPAGE
        self.FEES = FEES


    def worth(self, trading_coin_value):
        ## must  be called after removing the liquidated positions ( )
        return self.USDT_DISPO + self.COIN_DISPO * trading_coin_value + self.FUTURES_FREE + self.futures_worth(trading_coin_value=trading_coin_value)
    

    def futures_worth(self , trading_coin_value):
        # must remove the lown interest 
        futures_worth = 0
        for order in self.futures_open_orders:
            if order.is_long:
                futures_worth += order.openning_amount * (  (float(trading_coin_value) - order.openning_price)/ order.openning_price ) * order.leverage
            else:
                futures_worth -= order.openning_amount * (  (float(trading_coin_value) - order.openning_price)/ order.openning_price ) * order.leverage
        return futures_worth

    
    def liquidation(self, trading_coin_value_min , trading_coin_value_max , Report):
        if  self.FUTURES_IN_OERDER>0 and  self.futures_worth(trading_coin_value=trading_coin_value_min)<=0 :
            self.futures_open_orders.clear()
            Report.trace("LIQUIDATED")
            self.FUTURES_IN_OERDER = 0
            Report.trace(len(self.futures_open_orders))
            Report.signals(True , 0 ,trading_coin_value_min)
        if  self.FUTURES_IN_OERDER>0 and self.futures_worth(trading_coin_value=trading_coin_value_max)<=0 :
            self.futures_open_orders.clear()
            Report.trace("LIQUIDATED")
            self.FUTURES_IN_OERDER = 0
            Report.trace(len(self.futures_open_orders))
            Report.signals( True , 0  , trading_coin_value_max)


    def liquidation_price(self):
        
        # Lp = ( sum(amount(i) * leverage(i)) / sum( amount(i) * leverage(i) / openingP(i)))

        uper_therm = 0
        lower_therm  = 0

        for order in self.futures_open_orders:
            if order.is_long:
                uper_therm += order.openning_amount * order.leverage
                lower_therm += order.openning_amount * order.leverage / order.openning_price
            else:
                uper_therm -= order.openning_amount * order.leverage
                lower_therm -= order.openning_amount * order.leverage / order.openning_price
        if lower_therm !=0:
            return uper_therm/lower_therm
        else:
            return 0





    def buy(self , amount , price , Report ):
        execution_price = price * ( 1 + random.randrange(-1, 1) * random.random() * self.SLIPPAGE )
        if( self.USDT_DISPO > amount * execution_price + self.FEES ):
            self.USDT_DISPO -= amount * execution_price + self.FEES
            self.COIN_DISPO += amount
            Report.trace(f"buying -- wallet state =  usdt : {self.USDT_DISPO}, coin:{self.COIN_DISPO}")
            Report.signals(False , 1 , price)
            return execution_price
        else:
           Report.trace("insufficient balance")
           return -1
        

    def sell(self ,  amount , price , Report):
        execution_price = price * ( 1 + random.randrange(-1, 1) * random.random() * self.SLIPPAGE )
        if( self.COIN_DISPO > amount):
            self.USDT_DISPO += amount * execution_price - self.FEES
            self.COIN_DISPO -= amount
            Report.trace(f"selling -- wallet state =  usdt : {self.USDT_DISPO}, coin:{self.COIN_DISPO}")  
            Report.signals(False , -1  ,  price)
            return execution_price          
        else:
            Report.trace("insufficient balance")
            return -1
        


    def long(self , amount , price , leverage , Report):
        execution_price = price * ( 1 + random.randrange(-1, 1) *  random.random() * self.SLIPPAGE )
        if( self.FUTURES_FREE >= amount * execution_price + self.FEES):
            self.futures_open_orders.append( FuturesOrder(True , True , execution_price , amount , leverage=leverage ))
            self.FUTURES_FREE -= amount * execution_price + self.FEES
            self.FUTURES_IN_OERDER += 1
            Report.trace(f"long -- futures wallet open orders = {self.FUTURES_IN_OERDER} liquidation price {self.liquidation_price()}")  
            Report.signals(True , 1 , price)
            return execution_price          
        else:
            Report.trace("insufficient balance")
            return -1
        

    def short(self , amount , price , leverage , Report):
        execution_price = price * ( 1 + random.randrange(-1, 1) *  random.random() * self.SLIPPAGE )
        if( self.FUTURES_FREE >= amount * execution_price + self.FEES):
            self.futures_open_orders.append( FuturesOrder(False , True , execution_price , amount , leverage=leverage ))
            self.FUTURES_FREE -= amount * execution_price + self.FEES
            self.FUTURES_IN_OERDER += 1
            Report.trace(f"long -- futures wallet open orders = {self.FUTURES_IN_OERDER}")  
            Report.signals( True , -1 , price)
            return execution_price          
        else:
            Report.trace("insufficient balance")
            return -1
        
    def close_all_open_order(self  , price , Report):
        execution_price = price * ( 1 + random.randrange(-1, 1) *  random.random() * self.SLIPPAGE )
        worth = self.futures_worth(execution_price)
        self.futures_open_orders.clear()
        self.FUTURES_FREE += worth - self.FEES
        self.FUTURES_IN_OERDER = 0
        Report.trace("Futures orders closed")
        Report.signals(True , 0  , price)



   


