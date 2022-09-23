import random

class Agent:

    def __init__(self , wallet):
        # load existing agent or create new one 
       self.wallet = wallet
       
    def action(self , state , reward):
        #np.reshape(state , (4,12,-1)).transpose()
        amount=random.random()
        sell_buy_hold=random.choice([-1,0,1])
        return (amount,sell_buy_hold,self.TRADING_PAIR)


