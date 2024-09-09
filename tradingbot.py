from lumibot.brokers import Alpaca # broker 
from lumibot.backtesting import YahooDataBacktesting # backtesting framework
from lumibot.strategies.strategy import Strategy # actual trading bot
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST # market news
from timedelta import Timedelta
from finbert import estimate_sentiment
import torch 

API_KEY = 'PKUD332WAISYBL7U1KRI'
API_SECRET = 'W17F5HVvsp41WX2Ib1uHadRRQJP7qlsHoMBRtWf5'
BASE_URL = 'https://paper-api.alpaca.markets/v2'

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

class MLTrader(Strategy):
    def initialize(self, symbol:str='SPY',cash_at_risk:float=0.5):
        self.symbol = symbol #  must ammend for trading multiple stocks 
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL,key_id=API_KEY,secret_key=API_SECRET)

    def position_sizing(self):
        cash = self.get_cash() # get cash position
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity
    
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')
    

    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior,end=today)

        news = [ev.__dict__["_raw"]['headline']for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment



    def on_trading_iteration(self):
        current_date = self.get_datetime().date()
        if current_date == datetime(2023, 12, 29).date():
            print("End of backtest reached. Closing all positions...")
            self.sell_all()
            return  # End the iteration to avoid placing new trades on the last day
        
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment= self.get_sentiment()


        if cash > last_price:
                if sentiment == "positive" and probability > 0.999:
                    if self.last_trade == "sell":
                         self.sell_all() # if we have an existing sell order on a positive stock, sell that position
                    order = self.create_order(
                        self.symbol, 
                        quantity,
                        "buy",
                        type = "bracket",
                        take_profit_price=last_price*1.20, 
                        stop_loss_price = last_price*0.95
                    )
                    self.submit_order(order)
                    self.last_trade = "buy"

                elif sentiment == "negative" and probability > 0.999:
                    if self.last_trade == "buy":
                         self.sell_all()
                    order = self.create_order(
                        self.symbol, 
                        quantity,
                        "sell",
                        type = "bracket",
                        take_profit_price=last_price*0.80,
                        stop_loss_price = last_price*1.05
                    )
                    self.submit_order(order)
                    self.last_trade = "sell"

start_date = datetime(2020,1,1)  
end_date = datetime(2023,12,31)


broker = Alpaca(ALPACA_CREDS)

strategy = MLTrader(
    name='mlstrat', 
    broker=broker, 
    parameters={"symbol":"SPY", 
                "cash_at_risk":0.5}
    )


strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date,
    parameters={"symbol":"SPY",
                'cash_at_risk':0.5}
    )


# -156
# -383
# -718
# -1294
# -2184
# -1467
# - 891
# - 1676
# 1136
# -1 
# -251
# -621
# 587
# 7
# -221
# 7
# -210
# -546
# -1043
# -1767
# -934
# -1617
# -4262
# -6812
# 3907
# 7
# -1034
# 7
# -360
# 7
# -332
# 494
# -66
# -414
# -341
# -813
# -1535
# -2625
# -4246
# -6744
# -10439
# 5426
# 7
