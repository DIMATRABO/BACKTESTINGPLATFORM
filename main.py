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
HISTO_START=1664437575 # timestap to start backtesting from
HISTO_END = 1664438375 # timestap to stop backtestingmarket
CURRENT_TIME = HISTO_START
USDT_DISPO = 10000
COIN_DISPO = 0
FUTURES_BUDGET = 2000 #USDT

SLIPPAGE = 0.01 # %
LEVERAGE = 15 # %
 
FUTURES_ENTRY_PRICE = 1000 # USDT
FUTURES_ENTRY_AMOUNT = 1 # COIN
SPOT_ENTRY_AMOUNT = 1

SPOT_ENTRY_PRICE_percentage = 0.5
SPOT_SELL_PRICE_percentage = 0.4

profitable_percentage = 0.25 #%


ENTRY_PRICE = 1633.8
ENTRY_AMOUNT = 1

WALLET_EXCHANGE_FEE = 0.01 #USDT




# actions = [(ammount ,  sell_close_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_close_buy (-1,0,1) , is_market , is_futures , limit , leverage)]

def run_epoc( timestamp  , market , agent , wallet  ,report):
        state =  market.getState(timestamp, report)
        print(state)
        wallet.liquidation(state[3] , state[2] , report)
        actions = agent.action( state )
        market.execute(actions , timestamp , report)
        #report.plot(state , timestamp)

        
wallet=Wallet(TRADING_PAIR=TRADING_PAIR,USDT_DISPO=USDT_DISPO,COIN_DISPO=COIN_DISPO,FUTURES_FREE=FUTURES_BUDGET, SLIPPAGE=SLIPPAGE , FEES=WALLET_EXCHANGE_FEE )
market=Market(TRADING_PAIR=TRADING_PAIR, wallet=wallet)
agent=Agent(wallet = wallet, FUTURES_ENTRY_AMOUNT=FUTURES_ENTRY_AMOUNT , SPOT_ENTRY_AMOUNT=SPOT_ENTRY_AMOUNT , SPOT_ENTRY_PRICE_percentage=SPOT_ENTRY_PRICE_percentage , SPOT_SELL_PRICE_percentage= SPOT_SELL_PRICE_percentage , profitable_percentage = profitable_percentage , leverage=LEVERAGE)
        
report=Report()


if( IS_HISTORICAL_DATA ):

        while( CURRENT_TIME < HISTO_END ):
                run_epoc(CURRENT_TIME   , market=market , agent=agent ,wallet=wallet , report=report)
                CURRENT_TIME += TIME_STEP
        report.plot()

else:
        UTC=timezone('UTC')
        CURRENT_TIME=datetime.now(UTC).timestamp()
        run_epoc(CURRENT_TIME  , market , agent ,wallet , report)



