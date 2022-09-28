import mplfinance as mpf
import pandas as pd
from datetime import datetime
import numpy as np



class Report:
    candles = []
    buy_signals = []
    sell_signals = []
    liquidation_signals=[]

    def __init__(self ):
        self.candles = []
        self.buy_signals = []

    def trace(self ,message):
        print(message)

    def buy_signal(self , is_buy , price):
        if is_buy : 
            self.buy_signals.append(float(price))
        else : 
            self.buy_signals.append(np.nan)
    

    def signals(self , actions):
        is_buy = False
        if len(actions) == 0:
            self.buy_signal(is_buy ,0)
            return

        for action in actions:
            if action[1] == 1:
                is_buy = True
        
        self.buy_signal(is_buy , actions[0][4])



    def plot(self , state , timestamp):
        #t = int(state[0]/1000 )
        #t = round(t,0)
        time= datetime.fromtimestamp(timestamp, tz=None)
        D = time.strftime("%Y-%m-%d %H:%M:%S")   
        print(D)   
        #index = pd.DatetimeIndex(D)
        candel = [D , float(state[1]) , float(state[2]) , float(state[3]) , float(state[4]) , float(state[5])]
        self.candles.append(candel)
       
        df = pd.DataFrame(self.candles)
        df.rename(columns = {0:'Date', 1:'Open',2:'High' , 3:'Low', 4:'Close', 5:'Volume'}, inplace = True)
  
        df['Date'] = pd.to_datetime(df['Date']) 
        df = df.set_index('Date')
        #print(df)
        if float(state[2]) < 1633 :
            self.buy_signals.append(1633)
        else :
            self.buy_signals.append(-1)


        apds = [ 
         mpf.make_addplot(self.buy_signals,type='scatter',markersize=200,marker='^')
       ]



        mpf.plot(df, type="candle",   title = f" Price",  style="yahoo"  , hlines=dict( hlines=[1633.8,1620],colors=['g','r'],linestyle='-.'))