import yfinance as yf
import mplfinance as mpf
import os
from datetime import datetime

# NIFTY50 ka ticker symbol
#ticker = "^NSEI"
#FOR BANK NIFTY
ticker = "^NSEBANK"

# User se input lena period aur interval ke liye
period = input("Enter period (e.g., 1d, 5d, 1mo, 3mo, 6mo, 1y): ")
interval = input("Enter interval (e.g., 1m, 5m, 15m, 30m, 1h, 1d): ")

try:
    # Data fetch karna
    data = yf.download(ticker, period=period, interval=interval)

    # Check agar data empty to error handle karna
    if data.empty:
        print("No data found, please check the period or interval.")
    else:
        # Add a timestamp to the file name to make it unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"niftyBank_data_{period}_{interval}_{timestamp}.csv"
        file_path = os.path.join(os.getcwd(), file_name)  # Full file path
        
        # Data ko CSV file me save karna
        data.to_csv(file_path)
        
        # Success message with file path
        print(f"Data successfully downloaded and saved as {file_name}")
        print(f"File path: {file_path}")
        
        # Candlestick chart plot karna
        mpf.plot(data, type='candle', style='charles', title=f"Candlestick Chart ({period}, {interval})", volume=True)

except Exception as e:
    # Error handling if download fails
    print("Unsuccessful to download. Error: ", str(e))