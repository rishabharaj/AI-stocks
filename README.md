# Project

This directory contains various scripts related to stock market backtesting and analysis. Below is a brief description of each file in this directory.

## Files

### 1. `back930rule1.py`
This script implements a 9:15-9:30 rule for stock market backtesting. It includes:
- A class `NineFifteenRuleBacktest` with methods to apply the 9:15-9:30 rule and print results.
- Logic to identify breakouts, breakdowns, successful trades, and failed trades based on historical data.

### 2. `backtest2.py`
This script defines a trading strategy using moving averages and tracks separate profit/loss for trades. It includes:
- A class `MovingAverageCrossStrategy` with methods to execute buy/sell actions based on moving averages.
- Functionality to load historical data, set up backtesting, and display the results of trades.

### 3. `backtest3.py`
This script extends the moving average cross strategy to handle both long and short trades. It includes:
- A class `MovingAverageCrossStrategy` with methods to handle long and short trade signals.
- Functionality to calculate profit for both long and short trades and display the results.

### 4. `backtest4bestcondition.py`
This script optimizes moving average parameters for backtesting to find the best combination of short and long periods. It includes:
- A class `MovingAverageCrossStrategy` for the trading strategy.
- A loop to run backtests with different MA values and identify the best performing combination.

### 5. `backtesting1.py`
This script implements a backtesting strategy using moving averages and tracks the results. It includes:
- A class `MovingAverageCrossStrategy` with methods to execute buy/sell actions.
- Functionality to load data, set up backtesting, and display trade results in a candlestick chart.

### 6. `bitcoinlivedata.py`
This script fetches and plots real-time Bitcoin price data using `yfinance` and `mplfinance`. It includes:
- Functions to update the chart with real-time data and plot the candlestick chart.
- A button to refresh the data.

### 7. `dataBacktest.py`
This script fetches historical data for NIFTY50 or Bank NIFTY and saves it as a CSV file. It includes:
- User input for period and interval.
- Functionality to download data, save it to a CSV file, and plot a candlestick chart.

### 8. `optionchain.py`
This script fetches Nifty options chain data from the NSE website and displays it. It includes:
- Functionality to make a request to the NSE website and parse the JSON response.
- Logic to display call and put options data in a readable format and save it as CSV files.

### 9. `test1.py`
This script fetches historical data for NIFTY50 and plots a candlestick chart. It includes:
- User input for period and interval.
- Functionality to download data and plot a candlestick chart.

### 10. `test2.py`
This script fetches real-time market data using the `dhanhq` library. It includes:
- Initialization of the `DhanFeed` class with client ID and access token.
- Functionality to fetch and print real-time data for a specified instrument (e.g., HDFC Bank).

## Usage
Each script is designed to be run independently. Please refer to the comments within each script for specific instructions on how to use them.

## Requirements
- Python 3.x
- Required libraries: `os`, `pandas`, `backtrader`, `yfinance`, `mplfinance`, `numpy`, `requests`, `dhanhq`

To install the required libraries, you can use the following command:
```bash
pip install pandas backtrader yfinance mplfinance numpy requests dhanhq
```

## Conclusion
These scripts provide a comprehensive toolkit for backtesting and analyzing stock market data. Feel free to modify and extend them according to your needs.
