import os
import backtrader as bt
import yfinance as yf
import mplfinance as mpf
import pandas as pd
import numpy as np

# Step 1: Define the trading strategy with separate profit/loss tracking for both long and short trades
class MovingAverageCrossStrategy(bt.Strategy):
    params = (('short_period', 14), ('long_period', 26),)

    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        self.long_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)

        # Initialize trade tracking variables
        self.trade_count = 0
        self.successful_trades = 0
        self.failed_trades = 0
        self.total_profit = 0  # Track total profit in points
        self.total_loss = 0     # Track total loss in points
        self.total_gain = 0     # Track total gain in points
        self.entry_price = None
        self.entry_date = None  # Track the date of the entry (buy or short)
        self.is_long = False     # To distinguish between long and short trades

        # Track the positions for chart plotting
        self.buy_signals = []
        self.sell_signals = []
        self.successful_trades_points = []
        self.failed_trades_points = []

    def next(self):
        current_date = self.data.datetime.date(0)  # Get the current date
        if not self.position:  # Not in a position
            if self.short_ma > self.long_ma:  # Buy signal
                self.buy()
                self.is_long = True  # Mark as a long trade
                self.entry_price = self.data.close[0]  # Record the entry price
                self.entry_date = current_date  # Record the entry date
                self.trade_count += 1
                self.buy_signals.append(self.data.datetime.datetime(0).replace(tzinfo=None))  # Mark buy time for plotting
            elif self.short_ma < self.long_ma:  # Short signal
                self.sell()
                self.is_long = False  # Mark as a short trade
                self.entry_price = self.data.close[0]  # Record the entry price
                self.entry_date = current_date  # Record the entry date
                self.trade_count += 1
                self.sell_signals.append(self.data.datetime.datetime(0).replace(tzinfo=None))  # Mark sell time for plotting
        else:
            # Exit if the conditions reverse (long -> short or short -> long)
            if self.is_long and (self.short_ma < self.long_ma or current_date != self.entry_date):  # Exit long trade
                self.sell()  # Close long position
                exit_price = self.data.close[0]  # Record the exit price
                self.calculate_profit(exit_price)
            elif not self.is_long and (self.short_ma > self.long_ma or current_date != self.entry_date):  # Exit short trade
                self.buy()  # Close short position
                exit_price = self.data.close[0]  # Record the exit price
                self.calculate_profit(exit_price)

    def calculate_profit(self, exit_price):
        # Calculate profit/loss for the trade based on whether it was long or short
        if self.is_long:
            profit = exit_price - self.entry_price  # Profit for long trade
        else:
            profit = self.entry_price - exit_price  # Profit for short trade

        lot_size = 15  # Example: 15 units per lot (for BankNifty)
        profit *= lot_size  # Adjust profit by lot size

        # Update total profit and separate profits/losses
        if profit > 0:
            self.total_gain += profit
            self.successful_trades += 1
            self.successful_trades_points.append(self.data.datetime.datetime(0).replace(tzinfo=None))  # Mark success
        else:
            self.total_loss += abs(profit)
            self.failed_trades += 1
            self.failed_trades_points.append(self.data.datetime.datetime(0).replace(tzinfo=None))  # Mark failure

        # Update total profit/loss
        self.total_profit = self.total_gain - self.total_loss

# Step 2: Load the historical data from CSV
file_name = "nifty50_data_5d_5m_20240917_014831.csv"  # Replace with actual file name including .csv extension
file_path = os.path.join(os.getcwd(), file_name)  # Full path to the file

# Try to load the data
try:
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    data.index = data.index.tz_localize(None)  # Ensure the dataframe's index is timezone-naive
    print("Data loaded successfully!")
except FileNotFoundError:
    print(f"File not found: {file_path}. Please check the file name and location.")
    exit()  # Exit if the file is not found

# Convert the data into Backtrader-compatible feed
data_feed = bt.feeds.PandasData(dataname=data)

# Step 3: Set up Backtrader for backtesting
cerebro = bt.Cerebro()
strategies = cerebro.addstrategy(MovingAverageCrossStrategy)

# Add the data feed to cerebro
cerebro.adddata(data_feed)

# Set initial capital
cerebro.broker.setcash(100000)  # Initial capital set to 100,000

# Print starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Step 4: Run the backtest and retrieve the strategy instance
strategies = cerebro.run()
strategy = strategies[0]  # Get the instance of the first strategy

# Print ending portfolio value
print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Step 5: Display results of trades
print(f"Total trades taken: {strategy.trade_count}")
print(f"Successful trades: {strategy.successful_trades}")
print(f"Failed trades: {strategy.failed_trades}")
print(f"Total Gain points: {strategy.total_gain:.2f}")
print(f"Total Loss points: {strategy.total_loss:.2f}")
print(f"Net Profit (Total Points): {strategy.total_profit:.2f}")

# Step 6: Prepare marker data for plotting
# Create an empty array matching the data index for buy/sell markers
buy_marker = np.nan * np.ones(len(data))
sell_marker = np.nan * np.ones(len(data))
success_marker = np.nan * np.ones(len(data))
fail_marker = np.nan * np.ones(len(data))

# Populate the marker arrays at corresponding dates
for buy_time in strategy.buy_signals:
    buy_marker[data.index.get_loc(buy_time)] = data['Close'].loc[buy_time]

for sell_time in strategy.sell_signals:
    sell_marker[data.index.get_loc(sell_time)] = data['Close'].loc[sell_time]

for success_time in strategy.successful_trades_points:
    success_marker[data.index.get_loc(success_time)] = data['Close'].loc[success_time]

for fail_time in strategy.failed_trades_points:
    fail_marker[data.index.get_loc(fail_time)] = data['Close'].loc[fail_time]

# Step 7: Check if marker arrays are not empty and plot the candlestick chart
apdict = []
if not np.isnan(buy_marker).all():
    apdict.append(mpf.make_addplot(buy_marker, scatter=True, markersize=100, marker='^', color='g'))  # Buy markers
if not np.isnan(sell_marker).all():
    apdict.append(mpf.make_addplot(sell_marker, scatter=True, markersize=100, marker='v', color='r'))  # Sell markers
if not np.isnan(success_marker).all():
    apdict.append(mpf.make_addplot(success_marker, scatter=True, markersize=100, marker='o', color='b'))  # Successful trades
if not np.isnan(fail_marker).all():
    apdict.append(mpf.make_addplot(fail_marker, scatter=True, markersize=100, marker='x', color='y'))  # Failed trades

# Plot the candlestick chart with moving averages and markers
mpf.plot(data, type='candle', style='charles', title='Nifty 50 - Candlestick Chart with Backtesting',
         volume=True, mav=(14, 26), addplot=apdict)
