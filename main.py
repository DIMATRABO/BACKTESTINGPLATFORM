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
HISTO_START=1661261220 # timestap to start backtesting from
HISTO_END = 1661263941 # timestap to stop backtestingmarket
CURRENT_TIME = HISTO_START
USDT_DISPO = 10000
COIN_DISPO = 0
FUTURES_BUDGET = 10000 #USDT

SLIPPAGE = 0.01 # %
LEVERAGE = 1 # %
 
FUTURES_ENTRY_PRICE = 1000 # USDT
FUTURES_ENTRY_AMOUNT = 10 # COIN

ENTRY_PRICE = 1633.8
ENTRY_AMOUNT = 1

WALLET_EXCHANGE_FEE = 0.01 #USDT




# actions = [(ammount ,  sell_close_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_close_buy (-1,0,1) , is_market , is_futures , limit , leverage)]

def run_epoc( timestamp  , market , agent , wallet  ,report):
        state =  market.getState(timestamp)
        wallet.liguidation(state[3] , state[2] , report)
        actions = agent.action( state )
        market.execute(actions , timestamp , report)
        report.plot(state , timestamp)

        
wallet=Wallet(TRADING_PAIR=TRADING_PAIR,USDT_DISPO=USDT_DISPO,COIN_DISPO=COIN_DISPO,FUTURES_FREE=FUTURES_BUDGET, SLIPPAGE=SLIPPAGE , FEES=WALLET_EXCHANGE_FEE )
market=Market(TRADING_PAIR=TRADING_PAIR, wallet=wallet)
agent=Agent(wallet = wallet, ENTRY_PRICE_HIGH=ENTRY_PRICE ,ENTRY_PRICE_LOW=0 , ENTRY_AMOUNT = ENTRY_AMOUNT)
report=Report()


if( IS_HISTORICAL_DATA ):

        while( CURRENT_TIME < HISTO_END ):
                run_epoc(CURRENT_TIME   , market=market , agent=agent ,wallet=wallet , report=report)
                CURRENT_TIME += TIME_STEP

else:
        UTC=timezone('UTC')
        CURRENT_TIME=datetime.now(UTC).timestamp()
        run_epoc(CURRENT_TIME  , market , agent ,wallet , report)



