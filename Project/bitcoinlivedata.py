import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# BTC/USD ka ticker symbol
ticker = "BTC-USD"
#ticker = "^NSEI"
#ticker = "^NSEBANK"


# Create figure and axes for plotting
fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True)


# Create a new axes for the button
button_ax = plt.axes([0.81, 0.01, 0.1, 0.05])  # Position: [left, bottom, width, height]
refresh_button = Button(button_ax, 'Refresh', color='lightblue', hovercolor='lightgreen')

# Real-time data fetch karne ka function
def update_chart(event=None):
    try:
        # 5 minute ke interval me latest data fetch karna (last 1 day ka data)
        data = yf.download(ticker, period="1d", interval="5m")

        # Check if the data has been fetched properly
        if data.empty:
            print("No data available, skipping update.")
            return

        # Clear previous plots
        ax1.clear()
        ax2.clear()

        # Candlestick chart plot karna
        mpf.plot(data, type='candle', style='charles', ax=ax1, volume=ax2)

        # Latest live price fetch karna
        live_price = data['Close'][-1]

        # Latest candle ke open aur close prices nikalna
        last_candle = data.iloc[-1]  # Get the last row (most recent candle)
        open_price = last_candle['Open']
        close_price = last_candle['Close']

        # Candle ka color check karna
        if close_price > open_price:
            line_color = 'green'  # Candle is bullish (green)
        else:
            line_color = 'red'  # Candle is bearish (red)

        # Chart me live price ko show karna (horizontal line)
        ax1.axhline(live_price, color=line_color, linestyle='--', label=f'Live Price: ${live_price:.2f}')
        ax1.legend()

        # Chart title update karna
        ax1.set_title(f"BTC/USD Realtime Candlestick Chart (5-minute)\nLive Price: ${live_price:.2f}")

        # Redraw the figure with the updated chart
        fig.canvas.draw()

    except Exception as e:
        print(f"Error fetching or plotting data: {e}")

# Assign the button to the update_chart function
refresh_button.on_clicked(update_chart)

# Initial chart render
update_chart()

# Show the chart with refresh button
plt.show()