from datetime import datetime
from pytz import timezone    
from market import Market
from virtual_wallet import Wallet
from agent import Agent
from report import Report



TIME_STEP = 1  * 60 # on minuts
TRADING_PAIR="ETHUSDT"
IS_VIRTUAL_ENV=True
IS_HISTORICAL_DATA=True
HISTO_START=1661261166 # timestap to start backtesting from
HISTO_END = 1663939566 # timestap to stop backtestingmarket
CURRENT_TIME = HISTO_START
USDT_DISPO = 10000
COIN_DISPO = 1000
FUTURES_BUDGET = 1000 #USDT

SLIPPAGE = 0.01 # %
LEVERAGE = 15 # %
 
FUTURES_ENTRY_PRICE = 100 # USDT
FUTURES_ENTRY_AMOUNT = 100 # COIN




# actions = [(ammount ,  sell_hold_buy (-1,0,1) , is_market , is_futures , limit),(ammount ,   sell_hold_buy (-1,0,1) , is_market , is_futures , limit)]

def run_epoc( timestamp  , market , agent ,wallet ,report):
        state =  market.getState(timestamp)
        print(state[0][1])
        action = agent.action( state , wallet )
        #market.execute(action , wallet)
        #report.trace(action, wallet , timestamp)

        


wallet=Wallet(TRADING_PAIR=TRADING_PAIR,USDT_DISPO=USDT_DISPO,COIN_DISPO=COIN_DISPO,FUTURES_FREE=FUTURES_BUDGET, LEVERAGE=LEVERAGE , SLIPPAGE=SLIPPAGE )
market=Market(TRADING_PAIR=TRADING_PAIR, wallet=wallet)
agent=Agent(wallet = wallet)
report=Report()


if( IS_HISTORICAL_DATA ):

        while( CURRENT_TIME < HISTO_END ):
                run_epoc(CURRENT_TIME   , market=market , agent=agent ,wallet=wallet , report=report)
                CURRENT_TIME += TIME_STEP

else:
        UTC=timezone('UTC')
        CURRENT_TIME=datetime.now(UTC).timestamp()
        run_epoc(CURRENT_TIME  , market , agent)



