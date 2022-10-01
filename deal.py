from contextlib import closing


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

    def close(self , closing_time, closing_price , closing_wallet_worth ):
            self.closing_time = closing_time
            self.closing_price = closing_price
            self.closing_wallet_worth = closing_wallet_worth
            self.pnl = self.openning_wallet_worth - self.closing_wallet_worth
            self.pnl_percentage = self.pnl / self.openning_wallet_worth
            self.is_a_winning_deal = True if self.pnl>0 else False




        



