from typing import List
from openOrder import OpenOrder
from deal import Deal
from virtual_wallet import Wallet
class Agent:
    
    ordres : List[OpenOrder]
    FUTURES_ENTRY_AMOUNT: float

    SPOT_ENTRY_AMOUNT: float

    deals = List[Deal]

    losses = float

    SPOT_ENTRY_PRICE = float
    SPOT_ENTRY_PRICE_percentage = float

    SPOT_SELL_PRICE = float
    SPOT_SELL_PRICE_percentage = float

    profitable_percentage = float

    leverage = float

    liquidation = float






    def __init__(self , wallet , FUTURES_ENTRY_AMOUNT , SPOT_ENTRY_AMOUNT , SPOT_ENTRY_PRICE_percentage , SPOT_SELL_PRICE_percentage, profitable_percentage , leverage):
        self.wallet = wallet
        self.ordres = []
        self.FUTURES_ENTRY_AMOUNT = FUTURES_ENTRY_AMOUNT
        self.SPOT_ENTRY_AMOUNT = SPOT_ENTRY_AMOUNT
        self.deals = []
        self.losses = 0
        self.SPOT_ENTRY_PRICE = 0
        self.SPOT_ENTRY_PRICE_percentage = SPOT_ENTRY_PRICE_percentage
        self.SPOT_SELL_PRICE = 0
        self.SPOT_SELL_PRICE_percentage = SPOT_SELL_PRICE_percentage
        self.profitable_percentage = profitable_percentage
        self.leverage = leverage
        self.liquidation = 0







       #self.ordres.append( SpotOrder(False , ENTRY_PRICE_HIGH , None , ENTRY_AMOUNT/2))
       #self.ordres.append ( SpotOrder(True , None , ENTRY_PRICE_LOW , ENTRY_AMOUNT) )

    def action(self , state ):
        print(float(state[2]))
        if len(self.deals) > 0 and not self.deals[len(self.deals)-1].closing_time is None:
            pass


        else:
            # if there is no short order we create one 
            # actions = [(ammount ,  sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage)]   
            actions.append([self.FUTURES_ENTRY_AMOUNT , -1  , True , True , state[4], self.leverage])
            self.liquidation = self.wallet.liquidation_price_price(self,False, state[4] , self.leverage , 0)
            self.deals.append(Deal(state[0],state[4],self.wallet.worth(state[4]),None , None , None , None , None , False))

            self.SPOT_ENTRY_PRICE = ( self.SPOT_ENTRY_PRICE_percentage + 1 ) * 



                






        
        if len(self.ordres)==0:
             self.ordres.append ( SpotOrder(True , None , float(state[3]) , self.ENTRY_AMOUNT) )
             self.ordres.append( SpotOrder(False , 1.01 * float(state[3]) , None , self.ENTRY_AMOUNT/2))


        actions = []
        for order in self.ordres:
            if order.max_above_openning_high(state):
                 # actions = [(ammount ,  sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage)]
                actions.append([order.openning_amount , -1  , True , False , order.openning_price_high, 1])
                
                self.ordres.remove(order)
            
            if order.min_below_openning_low(state):
                 # actions = [(ammount ,  sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage)]
                actions.append([order.openning_amount , 1  , True , False , order.openning_price_low, 1])
                actions.append([order.openning_amount , -1  , True , True , order.openning_price_low , 15])
                self.ordres.remove(order)

            
        return actions


                
   