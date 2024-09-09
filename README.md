# Sentiment-Analysis-Trading-Bot
Sentiment Analysis Trading Bot using Lumibot and Alpaca API
This project implements a sentiment-driven trading algorithm that leverages news sentiment analysis to generate trading signals. The trading strategy uses Hugging Face's FinBERT model, which is fine-tuned for financial text classification, to analyze news sentiment for the SPY (S&P 500 ETF) over the past 3 days. Based on the sentiment (positive or negative), the bot takes long or short positions with a highly leveraged approach. The strategy was backtested over 4 years, achieving a 234% return, with most of the profit generated from short positions.

Key Features
Sentiment Analysis: Uses FinBERT to classify news headlines as positive, negative, or neutral.
Trading Strategy:
Go long on positive sentiment.
Go short on negative sentiment.
Positions are highly leveraged, allowing the bot to take full advantage of large movements.
Backtesting: The strategy was backtested using YahooDataBacktesting from Lumibot, covering SPY from January 1, 2020, to December 31, 2023.
Risk Management: Uses bracket orders with both take-profit and stop-loss prices to manage risk on each trade.
Results
Achieved a 234% return over 4 years, with most profits generated from short positions on SPY.
Highly leveraged positions allowed for larger gains, but also increased risk.
Prerequisites
To run this project, you need the following:

Python 3.8+
Lumibot for trading strategies and backtesting.
Alpaca API for news and trading operations.
Hugging Face Transformers for FinBERT sentiment analysis.
YahooDataBacktesting for historical data.
Setup
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/sentiment-trading-bot.git
cd sentiment-trading-bot
Install dependencies:

bash
Copy code
pip install lumibot alpaca_trade_api transformers torch
Configure Alpaca API keys in tradingbot.py:

python
Copy code
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
BASE_URL = 'https://paper-api.alpaca.markets/v2'
How It Works
Sentiment Analysis: The bot pulls financial news for SPY from Alpaca's news API for the past 3 days and uses FinBERT to classify the sentiment as positive, negative, or neutral.

Trading Decisions:

Positive sentiment: Bot enters a long position with a take-profit price set at 120% of the last traded price and a stop-loss at 95%.
Negative sentiment: Bot enters a short position with a take-profit price at 80% and a stop-loss at 105%.
The bot is allowed to take highly leveraged positions, risking up to 50% of the available cash.
Backtesting: The backtest runs from January 1, 2020, to December 31, 2023, and executes trades based on news sentiment at each iteration.

Example Code Snippets
Initializing the Trading Strategy
python
Copy code
class MLTrader(Strategy):
    def initialize(self, symbol='SPY', cash_at_risk=0.5):
        self.symbol = symbol
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)
Sentiment Analysis with FinBERT
python
Copy code
from finbert import estimate_sentiment

def get_sentiment():
    news = api.get_news(symbol='SPY', start=three_days_prior, end=today)
    headlines = [article.__dict__['_raw']['headline'] for article in news]
    probability, sentiment = estimate_sentiment(headlines)
    return probability, sentiment
Backtesting Results
Return: 234%
Time period: January 1, 2020 – December 31, 2023
Most profit: Generated from short positions on SPY based on negative sentiment.
Future Improvements
Extend to multiple stocks beyond SPY.
Incorporate additional technical indicators to improve decision-making.
Fine-tune the sentiment threshold for triggering trades.
