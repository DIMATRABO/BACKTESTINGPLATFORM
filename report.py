from doctest import debug_script
from socket import gaierror
import mplfinance as mpf
import pandas as pd
from datetime import datetime
import numpy as np



class Report:
    candles = []
    buy_signals = []
    sell_signals = []
    long_signals = []
    short_signals = []
    liquidation_signals=[]

    def __init__(self , debug_level ):
        self.candles = []
        self.buy_signals = []
        self.debug_level = debug_level

    def trace(self ,message , level):
        if self.debug_level >= level :
            print(message)

    def traceAction(self , action , level):
        if self.debug_level >= level :
            if len(action)>0:
                 print(action)


    def signals(self,is_futures ,  buy_close_sell, price):
        price = float(price)
        if buy_close_sell == -1 and not is_futures:
            self.sell_signals.append(price)

        if buy_close_sell == 0 :
            self.liquidation_signals.append(price)

        if buy_close_sell == 1 and not is_futures:
            self.buy_signals.append(price)

        if buy_close_sell == 1 and is_futures:
            self.long_signals.append(price)
        if buy_close_sell == -1 and is_futures:
            self.short_signals.append(price)

    def signals_refine(self):
        max = len(self.candles)
        if len(self.buy_signals) < max:
            self.buy_signals.append(np.nan)
        if len(self.sell_signals) < max:
            self.sell_signals.append(np.nan)

        if len(self.long_signals) < max:
            self.long_signals.append(np.nan)
        if len(self.short_signals) < max:
            self.short_signals.append(np.nan)
        
        if len(self.liquidation_signals) < max:
            self.liquidation_signals.append(np.nan)
        


    def add_candle(self , timestamp , state):
        time= datetime.fromtimestamp(timestamp, tz=None)
        D = time.strftime("%Y-%m-%d %H:%M:%S")  
        if self.debug_level >= 0: 
            print(D) 
        candel = [D , float(state[1]) , float(state[2]) , float(state[3]) , float(state[4]) , float(state[5])]
        self.candles.append(candel)






    def plot(self  , agent):
          
        df = pd.DataFrame(self.candles)
        df.rename(columns = {0:'Date', 1:'Open',2:'High' , 3:'Low', 4:'Close', 5:'Volume'}, inplace = True)
        df['Date'] = pd.to_datetime(df['Date']) 
        df = df.set_index('Date')
        apds = [ ]

        if np.nansum(self.liquidation_signals) > 0 :
            apds.append(mpf.make_addplot(self.liquidation_signals,type='scatter',markersize=300,marker='v',color='red'))

        if np.nansum(self.buy_signals) > 0 :
            apds.append(mpf.make_addplot(self.buy_signals,type='scatter',markersize=100,marker='^'))
        
        if np.nansum(self.sell_signals) > 0 :
            apds.append(mpf.make_addplot(self.sell_signals,type='scatter',markersize=100,marker='v',color='orange'))

        if np.nansum(self.long_signals) > 0 :
            apds.append(mpf.make_addplot(self.long_signals,type='scatter',markersize=100,marker='^' , color='green'))

        if np.nansum(self.short_signals) > 0 :
            apds.append(mpf.make_addplot(self.short_signals,type='scatter',markersize=100,marker='v' , color='violet'))


        if self.debug_level>=1:      
            print("----- buy --------")
            print(self.buy_signals)
            print(len(self.buy_signals))
            print(np.nansum(self.buy_signals))

            print("----- SELL --------")
            print(self.sell_signals)
            print(len(self.sell_signals))
            print(np.nansum(self.sell_signals))

            print("----- long --------")
            print(self.long_signals)
            print(len(self.long_signals))
            print(np.nansum(self.long_signals))

            print("----- short --------")
            print(self.short_signals)
            print(len(self.short_signals))
            print(np.nansum(self.short_signals))

            print("----- LIQUIDATED --------")
            print(self.liquidation_signals)
            print(len(self.liquidation_signals))
            print(np.nansum(self.liquidation_signals))


        print("__________________________________ Deals recap _______________________________________")
        print("_____________________________________________________________________________")
        print("__openning wallet worth __ closing wallet worth _____PNL______PNL % _____is winnig_")
        for deal in agent.deals:
            print(deal.to_string())
            wolletworth_1 = 0
            gain = 0
            for spotorder in deal.spot_orders :
                if  wolletworth_1 != 0 :
                    gain = (spotorder.openning_wallet_worth - wolletworth_1)/wolletworth_1
                print(spotorder.to_string() + f"----- delta= {round(gain,6)}%")
                wolletworth_1 = spotorder.openning_wallet_worth 


        #mpf.plot(df, type="candle",   title = f" Price",  style="yahoo"  , hlines=dict( hlines=[1633.8,1620],colors=['g','r'],linestyle='-.') ,addplot=apds )
        mpf.plot(df, type="candle", tight_layout = True ,   title = f" Price",  style="yahoo" ,addplot=apds )
        






