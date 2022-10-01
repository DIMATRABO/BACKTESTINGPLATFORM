from typing import List
from openOrder import OpenOrder
from deal import Deal
class Agent:
    
    ordres : List[OpenOrder]
    FUTURES_ENTRY_AMOUNT: float

    SPOT_ENTRY_AMOUNT: float

    deals : List[Deal]

    losses : float

    SPOT_ENTRY_PRICE : float
    SPOT_ENTRY_PRICE_percentage : float

    SPOT_SELL_PRICE : float
    SPOT_SELL_PRICE_percentage : float

    profitable_percentage : float

    closing_deal_price : float

    leverage : float

    liquidation : float

    nb_bought : int
    has_bougth : bool






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
        self.closing_deal_price = 0
        self.leverage = leverage
        self.liquidation = 0
        self.nb_bought = 0
        self.has_bougth = False







       #self.ordres.append( SpotOrder(False , ENTRY_PRICE_HIGH , None , ENTRY_AMOUNT/2))
       #self.ordres.append ( SpotOrder(True , None , ENTRY_PRICE_LOW , ENTRY_AMOUNT) )

    def action(self , state ):
        self.actions = []
        print(float(state[2]))
        if len(self.deals) > 0 and not self.deals[len(self.deals)-1].closing_time is None:
            for order in self.ordres:
                if order.min_below_openning_low(state):
                 # actions = [(ammount ,  sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage)]  
                    self.actions.append([order.openning_amount  , 1 , True , order.is_future  , order.openning_price_low , order.leverage ])
                if order.max_above_openning_high(state):
                    self.actions.append([order.openning_amount  , -1 , True , order.is_future , order.openning_price_low , order.leverage ])

                if state[3] <= self.closing_deal_price :
                    self.deals[len(self.deals)-1].close(state[0], self.closing_deal_price,self.wallet.worth(self.closing_deal_price))
                    self.ordres.clear()
                 
                if state[2] >= self.liquidation :
                    self.deals[len(self.deals)-1].close(state[0], self.liquidation ,self.wallet.worth(self.liquidation))
                    self.ordres.clear()
            
                if state[2] >= self.SPOT_ENTRY_PRICE  and  not self.has_bougth : 
                    # if the price gos above the spot buying price we create order to sell at liquidation price and to sell at spot sell price 
                    self.has_bougth = True
                    self.nb_bought += 1
                   
                    self.ordres.append( OpenOrder(False , False , self.liquidation , None , self.SPOT_ENTRY_AMOUNT , 1))
                    self.ordres.append( OpenOrder(False , False ,  None , self.SPOT_SELL_PRICE , self.SPOT_ENTRY_AMOUNT , 1))
                    




        else:
            # if there is no short order we create one 
            # actions = [(ammount ,  sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage)]   
            self.actions.append([self.FUTURES_ENTRY_AMOUNT , -1  , True , True , state[4], self.leverage])
            self.liquidation = self.wallet.liquidation_price_price(self,False, state[4] , self.leverage , 0)
            self.deals.append(Deal(state[0],state[4],self.wallet.worth(state[4]),None , None , None , None , None , False))

            # SPOT_ENTRY_PRICE_percentage should be between 0 and 1 
            self.SPOT_ENTRY_PRICE =  self.SPOT_ENTRY_PRICE_percentage  * ( self.liquidation - state[4] ) + state[4]
            # SPOT_SELL_PRICE_percentage should be between 0 and 1 and less then  SPOT_ENTRY_PRICE_percentage
            self.SPOT_SELL_PRICE =  self.SPOT_SELL_PRICE_percentage  * ( self.liquidation - state[4] ) + state[4]

            # profitable_percentage between 0 and 1  and leverage is int > 1 
            self.closing_deal_price = state[4]  * ( 1- self.profitable_percentage / self.leverage) 
            # add the spot buying order and the  future take profet order
            self.ordres.append( OpenOrder( True , False , self.SPOT_ENTRY_PRICE , None , self.SPOT_ENTRY_AMOUNT , 1))
            self.ordres.append(OpenOrder(False , True , None , self.closing_deal_price,self.FUTURES_ENTRY_AMOUNT, self.leverage))

            self.has_bougth = False
            self.nb_bought = 0


            




                






        
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


                
   