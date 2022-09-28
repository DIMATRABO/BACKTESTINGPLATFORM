from binance.client import Client
from datetime import datetime



class Market:
    api_key:str
    api_secret:str
    binance_client:Client()
    TRADING_PAIR:str    



    def __init__(self, TRADING_PAIR, wallet):
        # load existing env or create new one 
        self.TRADING_PAIR=TRADING_PAIR
        self.api_key="nmoso94nqqYndFWFKfyy0ZvsM0KexhvmrFCjmIboH1M15CYXpR8Qm0btrVKJbaj6"
        self.api_secret="zCILQLgeVkrUn3z9iBJ8RT4zrb07xfo561E7TmKkbHrvlsrYxnEw54FUYeoFkfA8"
        self.binance_client = Client(self.api_key, self.api_secret , tld='us')
        self.wallet=wallet


    def getState(self , timestamp):
        state = self.a_2min_of_1min_candles(timestamp=timestamp)
        return state[0] 

    def execute(self,actions,timestamp , report):
        # actions = [(ammount ,  sell_close_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_hold_buy (-1,0,1) , is_market , is_futures , limit , leverage)]
        if len(actions) > 0:
            for action in actions:
                if action[1] == 1 and action[3] == False:
                    self.wallet.buy( action[0] , action[4] , report )

                if action[1] == -1 and action[3] == False:
                    self.wallet.sell( action[0] , action[4] , report )

                if action[1] == 1 and  action[3] == True:
                    self.wallet.long(action[0] , action[4] , action[5] , report)

                if action[1] == -1 and  action[3] == True:
                    self.wallet.short(action[0] , action[4] , action[5] , report)

                


    def a_2min_of_1min_candles(self, timestamp):
        two_minutes_later= int(timestamp + 2*60)

        time1= datetime.fromtimestamp(timestamp, tz=None)
        time2= datetime.fromtimestamp(two_minutes_later, tz=None)
        
        date1=time1.strftime("%d %b, %Y %H:%M:%S")
        date2=time2.strftime("%d %b, %Y %H:%M:%S")
        return self.binance_client.get_historical_klines(self.TRADING_PAIR, Client.KLINE_INTERVAL_1MINUTE,str(date1),str(date2))


    def price_at_time(self , t):
        a_minute_ago = int(t - 60)
        time1= datetime.fromtimestamp(a_minute_ago, tz=None)
        time2= datetime.fromtimestamp(t, tz=None)
        date1=time1.strftime("%d %b, %Y %H:%M:%S")
        print(date1)
        date2=time2.strftime("%d %b, %Y %H:%M:%S")
        candle=self.binance_client.get_historical_klines(self.TRADING_PAIR, Client.KLINE_INTERVAL_1MINUTE,str(date1),str(date2))
        return (float(candle[0][1])+float(candle[0][4]))/2

    def date(self , t):
        time= datetime.fromtimestamp(t, tz=None)
        return time.strftime("%d %b, %Y %H:%M:%S")

