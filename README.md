# Sentiment-Analysis-Trading-Bot
This project implements a sentiment-driven trading algorithm that leverages news sentiment analysis to generate trading signals. The trading strategy uses Hugging Face's FinBERT model, which is fine-tuned for financial text classification, to analyze news sentiment for the SPY (S&P 500 ETF) over the past 3 days. Based on the sentiment (positive or negative), the bot takes long or short positions with a highly leveraged approach. The strategy was backtested over 4 years, achieving a 234% return, with most of the profit generated from short positions. <br><br><br>

![image](https://github.com/user-attachments/assets/8df3bc9c-3747-47f1-b9a3-2f81e70be144)



### Key Features
Sentiment Analysis: Uses FinBERT to classify news headlines as positive, negative, or neutral.<br>
Trading Strategy:<br>
<li>Go long on positive sentiment.<br>
<li>Go short on negative sentiment. <br>
<li>Positions are highly leveraged, allowing the bot to take full advantage of large movements.<br><br>
Backtesting: The strategy was backtested using YahooDataBacktesting from Lumibot, covering SPY from January 1, 2020, to December 31, 2023.<br>
Risk Management: Uses bracket orders with both take-profit and stop-loss prices to manage risk on each trade.<br><br>

### Results
Achieved a 234% return over 4 years, with most profits generated from short positions on SPY.<br>
Highly leveraged positions allowed for larger gains, but also increased risk. <br><br>

### Prerequisites
To run this project, you need the following:

<li>Python 3.8+
<li>Lumibot for trading strategies and backtesting.
<li>Alpaca API for news and trading operations.
<li>Hugging Face Transformers for FinBERT sentiment analysis.
<li>YahooDataBacktesting for historical data.<br><br>

<h2>Setup</h2>

<p>1. <strong>Clone the repository</strong>:</p>

<pre><code>git clone https://github.com/your-username/sentiment-trading-bot.git
cd sentiment-trading-bot
</code></pre>

<p>2. <strong>Install dependencies</strong>:</p>

<pre><code>pip install lumibot alpaca_trade_api transformers torch
</code></pre>

<p>3. <strong>Configure Alpaca API keys in <code>tradingbot.py</code></strong>:</p>

<pre><code>API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
BASE_URL = 'https://paper-api.alpaca.markets/v2'
</code></pre>

<hr>

<h2>How It Works</h2>

<h3>Sentiment Analysis</h3>
<p>The bot pulls financial news for SPY from Alpaca's news API for the past 3 days and uses FinBERT to classify the sentiment as positive, negative, or neutral.</p>

<h3>Trading Decisions</h3>
<ul>
  <li><strong>Positive sentiment</strong>: Bot enters a <strong>long</strong> position with a take-profit price set at 120% of the last traded price and a stop-loss at 95%.</li>
  <li><strong>Negative sentiment</strong>: Bot enters a <strong>short</strong> position with a take-profit price at 80% and a stop-loss at 105%.</li>
  <li>The bot is allowed to take highly leveraged positions, risking up to 50% of the available cash.</li>
</ul>

<h3>Backtesting</h3>
<p>The backtest runs from January 1, 2020, to December 31, 2023, and executes trades based on news sentiment at each iteration.</p>

<hr>

<h2>Example Code Snippets</h2>

<h3>Initializing the Trading Strategy</h3>
<pre><code>class MLTrader(Strategy):
    def initialize(self, symbol='SPY', cash_at_risk=0.5):
        self.symbol = symbol
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)
</code></pre>

<h3>Sentiment Analysis with FinBERT</h3>
<pre><code>from finbert import estimate_sentiment

def get_sentiment():
    news = api.get_news(symbol='SPY', start=three_days_prior, end=today)
    headlines = [article.__dict__['_raw']['headline'] for article in news]
    probability, sentiment = estimate_sentiment(headlines)
    return probability, sentiment
</code></pre>

<hr>

<h2>Backtesting Results</h2>
<ul>
  <li><strong>Return</strong>: 234%</li>
  <li><strong>Time period</strong>: January 1, 2020 – December 31, 2023</li>
  <li><strong>Most profit</strong>: Generated from <strong>short positions</strong> on SPY based on negative sentiment.</li>
</ul>

<hr>

<h2>Future Improvements</h2>
<ul>
  <li>Extend to multiple stocks beyond SPY.</li>
  <li>Incorporate additional technical indicators to improve decision-making.</li>
  <li>Fine-tune the sentiment threshold for triggering trades.</li>
</ul>

<hr>


