from typing import List
from spotOrder import SpotOrder
class Agent:
    
    ordres : List[SpotOrder]
    ENTRY_PRICE_HIGH : float
    ENTRY_PRICE_LOW : float
    ENTRY_AMOUNT: float

    def __init__(self , wallet , ENTRY_PRICE_HIGH , ENTRY_PRICE_LOW , ENTRY_AMOUNT):
       self.wallet = wallet
       self.ENTRY_PRICE_HIGH = ENTRY_PRICE_HIGH
       self.ENTRY_PRICE_LOW = ENTRY_PRICE_LOW
       self.ENTRY_AMOUNT = ENTRY_AMOUNT
       self.ordres = []
       self.ordres.append( SpotOrder(True , ENTRY_PRICE_HIGH , ENTRY_PRICE_LOW , ENTRY_AMOUNT))


    def action(self , state ):
        print(float(state[2]))
        actions = []
        for order in self.ordres:
            if order.max_above_openning_high(state):
                 # actions = [(ammount ,  sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage)]
                actions.append([order.openning_amount , 1  , True , False , order.openning_price_high, 1])
                actions.append([order.openning_amount , 1  , True , True , order.openning_price_high , 15])
                self.ordres.remove(order)
        return actions


                
   