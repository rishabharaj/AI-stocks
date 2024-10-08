import os
import pandas as pd

# Function to apply 9:15-9:30 rule for each day
class NineFifteenRuleBacktest:
    def __init__(self, df):
        self.df = df
        self.breakouts = []  # To store dates of breakouts
        self.breakdowns = []  # To store dates of breakdowns
        self.failed_trades = []  # To store dates of failed trades
        self.successful_trades = []  # To store dates of successful trades
        self.total_days = 0  # To store total number of days

    def apply_9_15_rule(self):
        # Group the data by day to apply the 9:15-9:30 rule per day
        self.df['date'] = self.df.index.date
        grouped = self.df.groupby('date')
        self.total_days = len(grouped)  # Count total number of days

        # Iterate over each day's data
        for date, day_data in grouped:
            # Step 1: Filter data for the first 15 minutes of the day
            day_data['time'] = day_data.index.time
            start_time = pd.Timestamp('09:15:00').time()
            end_time = pd.Timestamp('09:30:00').time()

            # Data between 9:15 and 9:30
            initial_range = day_data.between_time(start_time, end_time)

            if initial_range.empty:
                continue  # Skip if no data in the range

            # Calculate high and low of the first 15 minutes
            high_15 = initial_range['High'].max()
            low_15 = initial_range['Low'].min()

            # Step 2: After 9:30, check for breakout or breakdown for the rest of the day
            post_9_30 = day_data.loc[initial_range.index[-1]:]

            for i, (timestamp, row) in enumerate(post_9_30.iterrows()):
                if row['High'] > high_15:  # Breakout
                    self.breakouts.append((date, timestamp))  # Store breakout timestamp
                    # Check the next candle for success or failure
                    if i + 1 < len(post_9_30):
                        next_candle = post_9_30.iloc[i + 1]
                        if next_candle['Close'] < high_15:  # Failed trade
                            self.failed_trades.append((date, next_candle.name))
                        else:  # Successful trade
                            self.successful_trades.append((date, next_candle.name))
                    break  # Move to the next day after detecting a breakout
                elif row['Low'] < low_15:  # Breakdown
                    self.breakdowns.append((date, timestamp))  # Store breakdown timestamp
                    # Check the next candle for success or failure
                    if i + 1 < len(post_9_30):
                        next_candle = post_9_30.iloc[i + 1]
                        if next_candle['Close'] > low_15:  # Failed trade
                            self.failed_trades.append((date, next_candle.name))
                        else:  # Successful trade
                            self.successful_trades.append((date, next_candle.name))
                    break  # Move to the next day after detecting a breakdown

    def print_results(self):
        # Print dates of breakouts, breakdowns, successful and failed trades
        print(f"\nBreakout Dates: {self.breakouts}")
        print(f"Breakdown Dates: {self.breakdowns}")
        print(f"Successful Trade Dates: {self.successful_trades}")
        print(f"Failed Trade Dates: {self.failed_trades}")
        
        # Print summary
        print(f"\nSummary:")
        print(f"Total Breakouts: {len(self.breakouts)}")
        print(f"Total Breakdowns: {len(self.breakdowns)}")
        print(f"Total Successful Trades: {len(self.successful_trades)}")
        print(f"Total Failed Trades: {len(self.failed_trades)}")
        print(f"Total Number of Days: {self.total_days}")

# Step 3: Load the CSV file (prompt user for input)
file_name = input("Enter the name of the CSV file (including the extension): ")

# Check if the file exists and load it
if os.path.exists(file_name):
    df = pd.read_csv(file_name, parse_dates=['Datetime'], index_col='Datetime')
    print(f"CSV file loaded: {file_name}")

    # Initialize the NineFifteenRuleBacktest with the DataFrame
    backtest = NineFifteenRuleBacktest(df)

    # Apply the 9:15-9:30 rule
    backtest.apply_9_15_rule()

    # Print the results (dates of breakouts, successes, and failures)
    backtest.print_results()

else:
    print("CSV file not found. Please check the file name and try again.")
