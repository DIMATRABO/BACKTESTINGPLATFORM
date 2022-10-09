
from spotExecutedOrder import SpotExecutedOrder


class Deal:

    openning_time = float
    openning_price = float
    openning_wallet_worth = float
    closing_time = float
    closing_price = float
    closing_wallet_worth = float
    pnl = float
    pnl_percentage = float
    is_a_winning_deal = bool
    



    def __init__(self , openning_time , openning_price,  openning_wallet_worth , closing_time, closing_price , closing_wallet_worth , pnl, pnl_percentage  ,  is_a_winning_deal ):
            self.openning_time = openning_time
            self.openning_price = openning_price
            self.openning_wallet_worth = openning_wallet_worth
            self.closing_time = closing_time
            self.closing_price = closing_price
            self.closing_wallet_worth = closing_wallet_worth
            self.pnl = pnl
            self.pnl_percentage = pnl_percentage
            self.is_a_winning_deal = is_a_winning_deal
            self.spot_orders = list[SpotExecutedOrder]

    def close(self , closing_time, closing_price , closing_wallet_worth ):
            self.closing_time = closing_time
            self.closing_price = closing_price
            self.closing_wallet_worth = closing_wallet_worth
            self.pnl = self.closing_wallet_worth - self.openning_wallet_worth 
            self.pnl_percentage = self.pnl / self.openning_wallet_worth
            self.is_a_winning_deal = True if self.pnl>0 else False



    def to_string(self):

        """ to_return =  f" openning_price = {self.openning_price} "
        if not self.closing_time is None:
            to_return +=  f"  closing_price = {self.closing_price} "
        else :
             to_return +=  f" -- deal non closed"

        
        to_return += f" openning_wallet_worth = {self.openning_wallet_worth}"
        if not self.closing_time is None:
            to_return +=  f" closing_wallet_worth = {self.closing_wallet_worth} "
            to_return += f"  pnl = {self.pnl} pnl_percentage = {self.pnl_percentage} %  is_a_winning_deal = { 1 if self.is_a_winning_deal else 0}"
        return to_return
        """
        w_close = "       _ "
        pnl ="   _  "
        pnl_p="   _  "
        w = ' _ '
        if not self.closing_time is None:
            w_close = round(self.closing_wallet_worth,3)
            pnl = round(self.pnl,3)
            pnl_p=round(self.pnl_percentage,2)
            w = self.is_a_winning_deal


            


        self.closing_wallet_worth
        return f"_  {round(self.openning_wallet_worth,3)}$               |       {w_close}$       |  {pnl}$  | {pnl_p}% | {w}"