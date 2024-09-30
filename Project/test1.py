import yfinance as yf
import mplfinance as mpf

# NIFTY50 ka ticker symbol
ticker = "^NSEI"

# User se input lena period aur interval ke liye
period = input("Enter period (e.g., 1d, 5d, 1mo, 3mo, 6mo, 1y): ")
interval = input("Enter interval (e.g., 1m, 5m, 15m, 30m, 1h, 1d): ")

# Data fetch karna
data = yf.download(ticker, period=period, interval=interval)

# Check agar data empty to error handle karna
if data.empty:
    print("No data found, please check the period or interval.")
else:
    # Candlestick chart plot karna
    mpf.plot(data, type='candle', style='charles', title=f"NIFTY50 Candlestick Chart ({period}, {interval})", volume=True)