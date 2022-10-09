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

    liquidation_price = float
 

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

        self.liquidation_price = self.liquidation_price_calc()


    def worth(self, trading_coin_value):
        ## must  be called after removing the liquidated positions ( )
        trading_coin_value = float(trading_coin_value)
        return self.USDT_DISPO + self.COIN_DISPO * trading_coin_value  + self.futures_worth(trading_coin_value=trading_coin_value)
    

    def futures_worth(self , trading_coin_value):
        # must remove the lown interest 
        trading_coin_value = float(trading_coin_value)
        futures_worth = self.FUTURES_FREE
        for order in self.futures_open_orders:
            if order.is_long:
                futures_worth += order.openning_amount/order.openning_price * (  (float(trading_coin_value) - order.openning_price)/ order.openning_price ) * order.leverage
            else:
                futures_worth -= order.openning_amount/order.openning_price * (  (float(trading_coin_value) - order.openning_price)/ order.openning_price ) * order.leverage
        return futures_worth

    def sum_futures_amounts(self):
        futures_amounts = 0
        for order in self.futures_open_orders:
            if order.is_long:
                futures_amounts -= order.openning_amount 
            else:
                futures_amounts += order.openning_amount 
        return futures_amounts

    
    
    def liquidation_price_calc(self):
        # Lp = ( sum(amount(i) * leverage(i)) / sum( amount(i) * leverage(i) / openingP(i)))
        uper_therm = 1
        lower_therm  = 0
        for order in self.futures_open_orders:
            if order.is_long:
                uper_therm +=  order.leverage
                lower_therm += order.leverage / order.openning_price       
            else:
                uper_therm += order.leverage
                lower_therm +=  order.leverage / order.openning_price
    
        
        if lower_therm !=0:
            return  (1 + uper_therm)/lower_therm
        else:
            return 0


    def pnl_percentage(self , price):
        sum_  = 0
        for order in self.futures_open_orders:
            if order.is_long:
                sum_ += order.leverage * (float(price) - order.openning_price)/order.openning_price    
            else:
                sum_ += order.leverage * (order.openning_price - float(price) )/order.openning_price    
    
        return sum_



    def liquidation(self, trading_coin_value_min , trading_coin_value_max , Report):
        """
        if  self.FUTURES_IN_OERDER>0 and  self.pnl_percentage(trading_coin_value_min)<=-1 :
            Report.trace("LIQUIDATED")
            Report.signals(True , 0 ,self.liquidation_price)
            self.futures_open_orders.clear()
            self.FUTURES_IN_OERDER = 0

        if  self.FUTURES_IN_OERDER>0 and self.pnl_percentage(trading_coin_value_max)<=-1 :
            Report.trace("LIQUIDATED")
            Report.signals( True , 0  , self.liquidation_price)
            self.futures_open_orders.clear()
            self.FUTURES_IN_OERDER = 0
        """
        if  self.FUTURES_IN_OERDER>0 and  self.liquidation_price <= float(trading_coin_value_max) :
            Report.trace("LIQUIDATED")
            Report.signals(True , 0 ,self.liquidation_price)
            self.futures_open_orders.clear()
            self.FUTURES_IN_OERDER = 0
            






    def liquidation_price_price(self,is_long, price , leverage , fee):
        # fee should be between 0 and 1 
        if is_long :
            liq =  float(price)*( 1 - (1 - fee)/leverage)
            self.liquidation_price = liq        
            return liq
        else :
            liq = float(price) *( 1 + (1 - fee)/leverage)
            self.liquidation_price = liq
            return liq






    def buy(self , amount , price , Report ):
        price = float(price)
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
        price = float(price)
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
        


    def long(self , amount_usdt , price , leverage , Report):
        price = float(price)
        execution_price = price * ( 1 + random.randrange(-1, 1) *  random.random() * self.SLIPPAGE )
        if( self.sum_futures_amounts() >= amount_usdt + self.FEES):
            self.FUTURES_FREE += self.futures_worth(price)
            for f_order in self.futures_open_orders:
                if not f_order.is_long:
                    self.futures_open_orders.remove(f_order)
            self.FUTURES_IN_OERDER -= 1
            Report.trace(f"long -- futures wallet open orders = {self.FUTURES_IN_OERDER} liquidation price {self.liquidation_price_calc()} ---> {self.liquidation_price}")  
            Report.signals(True , 1 , price)
            return execution_price 

        elif( self.FUTURES_FREE >= amount_usdt + self.FEES):
            self.futures_open_orders.append( FuturesOrder(True , True , execution_price , amount_usdt , leverage=leverage ))
            self.FUTURES_FREE -= amount_usdt + self.FEES
            self.FUTURES_IN_OERDER += 1
            Report.trace(f"long -- futures wallet open orders = {self.FUTURES_IN_OERDER} liquidation price {self.liquidation_price_calc()} ---> {self.liquidation_price}")  
            Report.signals(True , 1 , price)
            return execution_price          
        else:
            Report.trace("insufficient balance")
            return -1
        

    def short(self , amount_usdt , price , leverage , Report):
        price = float(price)
        execution_price = price * ( 1 + random.randrange(-1, 1) *  random.random() * self.SLIPPAGE )
        if( self.FUTURES_FREE >= amount_usdt + self.FEES):
            self.futures_open_orders.append( FuturesOrder(False , True , execution_price , amount_usdt , leverage=leverage ))
            self.FUTURES_FREE -= amount_usdt  + self.FEES
            self.FUTURES_IN_OERDER += 1
            Report.trace(f"short -- futures wallet open orders = {self.FUTURES_IN_OERDER} liquidation price {self.liquidation_price_calc()} ---> {self.liquidation_price}")  
            Report.signals( True , -1 , price)
            return execution_price          
        else:
            Report.trace("insufficient balance")
            return -1
        
    def close_all_open_order(self  , price , Report):
        price = float(price)
        execution_price = price * ( 1 + random.randrange(-1, 1) *  random.random() * self.SLIPPAGE )
        worth = self.futures_worth(execution_price)
        self.futures_open_orders.clear()
        self.FUTURES_FREE += worth - self.FEES
        self.FUTURES_IN_OERDER = 0
        Report.trace("Futures orders closed")
        Report.signals(True , 0  , price)



   


