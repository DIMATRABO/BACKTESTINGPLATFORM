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
HISTO_END = 1664474995 # timestap to stop backtestingmarket
CURRENT_TIME = HISTO_START
USDT_DISPO = 40000
COIN_DISPO = 0
FUTURES_BUDGET = 4000#USDT

SLIPPAGE = 0# %
LEVERAGE = 100 # x
 

FUTURES_ENTRY_AMOUNT_USDT = 10 # $
SPOT_DESIRED_PROFIT = 10 # USDT



SPOT_ENTRY_PRICE_percentage = 0.2
SPOT_SELL_PRICE_percentage = 0.1

profitable_percentage = 2.5 #% FUTURES 

WALLET_EXCHANGE_FEE = 0.1 #USDT

debug = True






# actions = [(ammount ,  sell_close_buy (-1,0,1) , is_market , is_futures , limit , leverage),(ammount ,   sell_close_buy (-1,0,1) , is_market , is_futures , limit , leverage)]

def run_epoc( timestamp  , market , agent , wallet  ,report):
        
        state =  market.getState(timestamp, report)
        report.trace(state)
        wallet.liquidation(state[3] , state[2] , report)
        agent.start_spot_wallet_worth_calc(state[1],wallet.USDT_DISPO , wallet.COIN_DISPO)
        actions = agent.action( state , report )
        report.trace(actions)
        market.execute(actions , timestamp , report)

        #report.plot(state , timestamp)

        
wallet=Wallet(TRADING_PAIR=TRADING_PAIR,USDT_DISPO=USDT_DISPO,COIN_DISPO=COIN_DISPO,FUTURES_FREE=FUTURES_BUDGET, SLIPPAGE=SLIPPAGE , FEES=WALLET_EXCHANGE_FEE )
market=Market(TRADING_PAIR=TRADING_PAIR, wallet=wallet)
agent=Agent(wallet = wallet, FUTURES_ENTRY_AMOUNT_USDT=FUTURES_ENTRY_AMOUNT_USDT , SPOT_DESIRED_PROFIT=SPOT_DESIRED_PROFIT , SPOT_ENTRY_PRICE_percentage=SPOT_ENTRY_PRICE_percentage , SPOT_SELL_PRICE_percentage= SPOT_SELL_PRICE_percentage , profitable_percentage = profitable_percentage , leverage=LEVERAGE)
        
report=Report(debug)


if( IS_HISTORICAL_DATA ):
        
        while( CURRENT_TIME < HISTO_END ):
                run_epoc(CURRENT_TIME   , market=market , agent=agent ,wallet=wallet , report=report)
                CURRENT_TIME += TIME_STEP
        report.plot(agent)
        

else:
        UTC=timezone('UTC')
        CURRENT_TIME=datetime.now(UTC).timestamp()
        run_epoc(CURRENT_TIME  , market , agent ,wallet , report)




