import os
import backtrader as bt
import pandas as pd
import numpy as np

# Step 1: Define the trading strategy with profit/loss tracking
class MovingAverageCrossStrategy(bt.Strategy):
    params = (('short_period', 14), ('long_period', 50),)

    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        self.long_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)

        # Initialize trade tracking variables
        self.trade_count = 0
        self.successful_trades = 0
        self.failed_trades = 0
        self.total_profit = 0  # Track total profit in ₹
        self.total_loss = 0     # Track total loss in ₹
        self.total_gain = 0     # Track total gain in ₹
        self.entry_price = None
        self.entry_date = None  # Track the date of the entry (buy)

    def next(self):
        current_date = self.data.datetime.date(0)  # Get the current date
        if not self.position:  # Not in a position
            if self.short_ma > self.long_ma:  # Buy signal
                self.buy()
                self.entry_price = self.data.close[0]  # Record the entry price
                self.entry_date = current_date  # Record the entry date
                self.trade_count += 1
        else:
            # Exit if the short MA crosses below the long MA or if it's the end of the day
            if self.short_ma < self.long_ma or current_date != self.entry_date:  # Sell signal or different day
                self.sell()
                exit_price = self.data.close[0]  # Record the exit price

                # Calculate profit/loss for this trade
                profit = exit_price - self.entry_price  # Profit in price points

                # If you're trading multiple lots, multiply the profit by the lot size
                lot_size = 15  # Example: 15 units per lot (for BankNifty)
                profit = profit * lot_size  # Adjust profit by lot size

                # Update total profit and separate profits/losses
                if profit > 0:
                    self.total_gain += profit
                    self.successful_trades += 1
                else:
                    self.total_loss += abs(profit)
                    self.failed_trades += 1

                # Update total profit/loss
                self.total_profit = self.total_gain - self.total_loss

# Step 2: Load the historical data from CSV
# Request user input for file name
file_name = input("Enter the name of the CSV file (including the extension): ")

# Automatically detect the file path in the same folder or parent folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# First check in the current directory
file_path = os.path.join(current_dir, file_name)

# If not found, check in the parent directory
if not os.path.isfile(file_path):
    file_path = os.path.join(parent_dir, file_name)

# Try to load the data
try:
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    data.index = data.index.tz_localize(None)  # Ensure the dataframe's index is timezone-naive
    print("Data loaded successfully!")
except FileNotFoundError:
    print(f"File not found: {file_path}. Please check the file name and location.")
    exit()  # Exit if the file is not found

# Step 3: Define the function to run the backtest
def run_backtest(short_period, long_period):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MovingAverageCrossStrategy, short_period=short_period, long_period=long_period)

    # Convert the data into Backtrader-compatible feed
    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    # Set initial capital
    cerebro.broker.setcash(100000)

    # Run the backtest
    strategies = cerebro.run()
    strategy = strategies[0]

    # Return the net profit and total trades
    return strategy.total_profit, strategy.trade_count, strategy.successful_trades, strategy.failed_trades

# Step 4: Run the optimization loop for best MA values
best_profit = -float('inf')
best_short_ma = None
best_long_ma = None
best_trade_count = 0
best_successful_trades = 0
best_failed_trades = 0

for short_ma in range(5, 20):  # Short MA from 5 to 20
    for long_ma in range(50, 101):  # Long MA from 50 to 100
        net_profit, trade_count, successful_trades, failed_trades = run_backtest(short_ma, long_ma)
        
        if net_profit > best_profit:
            best_profit = net_profit
            best_short_ma = short_ma
            best_long_ma = long_ma
            best_trade_count = trade_count
            best_successful_trades = successful_trades
            best_failed_trades = failed_trades

# Step 5: Print the best result
print(f"Best Combination: Short MA = {best_short_ma}, Long MA = {best_long_ma}")
print(f"Net Profit: {best_profit:.2f}")
print(f"Total Trades: {best_trade_count}")
print(f"Successful Trades: {best_successful_trades}")
print(f"Failed Trades: {best_failed_trades}")
print(f"Success Rate: {best_successful_trades / best_trade_count:.2f}" if best_trade_count > 0 else "No trades taken")
