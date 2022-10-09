from typing import List
from openOrder import OpenOrder
from deal import Deal
from report import Report
class Agent:
    
    ordres : List[OpenOrder]
    FUTURES_ENTRY_AMOUNT_USDT: float

    SPOT_DESIRED_PROFIT: float

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

    start_spot_wallet_worth = 0
    first_execution = True





    def __init__(self , wallet , FUTURES_ENTRY_AMOUNT_USDT , SPOT_DESIRED_PROFIT , SPOT_ENTRY_PRICE_percentage , SPOT_SELL_PRICE_percentage, profitable_percentage , leverage):
        
        self.wallet = wallet
        self.ordres = []
        self.FUTURES_ENTRY_AMOUNT_USDT = FUTURES_ENTRY_AMOUNT_USDT
        self.SPOT_DESIRED_PROFIT = SPOT_DESIRED_PROFIT
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
        self.SPOT_ENTRY_AMOUNT=0



    def start_spot_wallet_worth_calc(self , start_price ,USDT_DISPO , COIN_DISPO):
        if self.first_execution:
                self.first_execution = False
                self.start_spot_wallet_worth = USDT_DISPO + COIN_DISPO * float(start_price)
                return  self.start_spot_wallet_worth




       #self.ordres.append( SpotOrder(False , ENTRY_PRICE_HIGH , None , ENTRY_AMOUNT/2))
       #self.ordres.append ( SpotOrder(True , None , ENTRY_PRICE_LOW , ENTRY_AMOUNT) )

    def action(self , state ,report ):
        self.actions = []
     
       
        if len(self.deals) > 0 and self.deals[len(self.deals)-1].closing_time is None:
            for order in self.ordres:
                if order.min_below_openning_low(state):
                 # actions = [(ammount ,  sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage)]  
                    self.actions.append([order.openning_amount  , 1 if order.is_buy else -1 , True , order.is_future  , order.openning_price_low , order.leverage ])
                    self.ordres.remove(order)

                if order.max_above_openning_high(state):
                    self.actions.append([order.openning_amount  , 1 if order.is_buy else -1 , True , order.is_future , order.openning_price_high , order.leverage ])
                    self.ordres.remove(order)


            report.trace( f"closing deal price = {self.closing_deal_price } liquidation price = {self.liquidation} SPOT_ENTRY_PRICE = {self.SPOT_ENTRY_PRICE} SPOT_SELL_PRICE = {self.SPOT_SELL_PRICE}")

            if float(state[3]) <= self.closing_deal_price :
                    #Take profit
                    self.deals[len(self.deals)-1].close(state[0], self.closing_deal_price,self.wallet.worth(self.closing_deal_price))
                    self.ordres.clear()
                 
            if float(state[2]) >= self.liquidation :
                    self.deals[len(self.deals)-1].close(state[0], self.liquidation ,self.wallet.worth(self.liquidation))
                    self.ordres.clear()
            
            if float(state[2]) >= self.SPOT_ENTRY_PRICE  and  not self.has_bougth : 
                    # if the price gos above the spot buying price we create order to sell at liquidation price and to sell at spot sell price 
                    self.has_bougth = True
                    self.nb_bought += 1
                   
                   # recalculate the spot entry ammount 
                    self.spotEntryAmountCalc()
                   
                    self.ordres.append( OpenOrder(False , False , self.liquidation , None , self.SPOT_ENTRY_AMOUNT , 1))
                    self.ordres.append( OpenOrder(False , False ,  None , self.SPOT_SELL_PRICE , self.SPOT_ENTRY_AMOUNT , 1))

            if float(state[3]) <= self.SPOT_SELL_PRICE  and  self.has_bougth : 
                    # if the price gos bellow the spot selling price we create order to buy at spot buy price with higher ammount
                    self.has_bougth = False
                    for order in self.ordres:
                        if order.openning_price_high == self.liquidation:
                            self.ordres.remove(order)
                            
                    self.losses -= ( self.SPOT_ENTRY_AMOUNT * ( self.SPOT_SELL_PRICE - self.SPOT_ENTRY_PRICE)/self.SPOT_ENTRY_PRICE )- self.wallet.FEES

                    # recalculate the spot entry ammount 
                    self.spotEntryAmountCalc()

                    self.ordres.append( OpenOrder(True , False ,  self.SPOT_ENTRY_PRICE , None , self.SPOT_ENTRY_AMOUNT , 1))
                    

                     

        else:
            # if there is no short order we create one 
            # actions = [(ammount ,  sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage)]   
            self.actions.append([self.FUTURES_ENTRY_AMOUNT_USDT , -1  , True , True , state[4], self.leverage])
            self.liquidation = self.wallet.liquidation_price_price(False, state[4] , self.leverage , 0)
            self.deals.append(Deal(state[0],state[4],self.wallet.worth(state[4]),None , None , None , None , None , False))

            # SPOT_ENTRY_PRICE_percentage should be between 0 and 1 
            self.SPOT_ENTRY_PRICE =  self.SPOT_ENTRY_PRICE_percentage  * ( self.liquidation - float(state[4]) ) + float(state[4])
            # SPOT_SELL_PRICE_percentage should be between 0 and 1 and less then  SPOT_ENTRY_PRICE_percentage
            self.SPOT_SELL_PRICE =  self.SPOT_SELL_PRICE_percentage  * ( self.liquidation - float(state[4]) ) + float(state[4])

            #calculate the spot entry ammount 
            self.spotEntryAmountCalc()

            # profitable_percentage between 0 and 1  and leverage is int > 1 
            self.closing_deal_price = float(state[4])  * ( 1- self.profitable_percentage / self.leverage) 
            # add the spot buying order and the  future take profet order
            self.ordres.append( OpenOrder( True , False , self.SPOT_ENTRY_PRICE , None , self.SPOT_ENTRY_AMOUNT , 1))
            self.ordres.append(OpenOrder(True , True , None , self.closing_deal_price,self.FUTURES_ENTRY_AMOUNT_USDT, self.leverage))
            # OpenOrder(is_buy , is_future, openning_price_high, openning_price_low , openning_amount, leverage)
       
            self.has_bougth = False
            self.nb_bought = 0

        return self.actions


            




                
    def increaseSpotBuyAmount(self):
        #return self.SPOT_ENTRY_AMOUNT * self.nb_bought * self.losses 
        return self.SPOT_ENTRY_AMOUNT + self.losses

    def spotEntryAmountCalc(self):
        liquidation = self.liquidation
        desired_profit = self.SPOT_DESIRED_PROFIT  
        Futures_EA = self.FUTURES_ENTRY_AMOUNT_USDT 
        fees = self.losses
        # x = Futures_EA/(DProfit+fees*(LiqP/Futures_EA)     
        x = Futures_EA/(desired_profit + fees*(liquidation / Futures_EA))
        self.SPOT_ENTRY_AMOUNT = x
        return x
        




