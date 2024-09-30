import requests
import pandas as pd

# URL to fetch the Nifty options chain data
url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY",
    "Host": "www.nseindia.com",
}

# Make a request to the NSE website
session = requests.Session()

try:
    response = session.get(url, headers=headers)
    
    # Check if response was successful
    if response.status_code == 200:
        print("Data fetched successfully!")
        data = response.json()

        # Extract the relevant data from the JSON response
        records = data['records']['data']
        
        # Prepare empty lists to store call and put option data
        calls_data = []
        puts_data = []

        # Loop through the records and append call and put data to respective lists
        for record in records:
            if 'CE' in record:  # Check if call option (CE) data exists
                calls_data.append(record['CE'])
            if 'PE' in record:  # Check if put option (PE) data exists
                puts_data.append(record['PE'])

        # Convert lists into Pandas DataFrames
        calls_df = pd.DataFrame(calls_data)
        puts_df = pd.DataFrame(puts_data)

        # Select relevant columns to display
        calls_df = calls_df[['strikePrice', 'lastPrice', 'openInterest', 'changeinOpenInterest', 'totalTradedVolume']]
        puts_df = puts_df[['strikePrice', 'lastPrice', 'openInterest', 'changeinOpenInterest', 'totalTradedVolume']]

        # Sort DataFrames by strike price for better readability
        calls_df = calls_df.sort_values(by='strikePrice')
        puts_df = puts_df.sort_values(by='strikePrice')

        # Display the first 10 rows of each DataFrame
        print("\nCall Options Data:")
        print(calls_df.head(10))  # Show the first 10 rows of the call options

        print("\nPut Options Data:")
        print(puts_df.head(10))  # Show the first 10 rows of the put options

        # Optionally save data to CSV if needed
        calls_df.to_csv("nifty_calls_data.csv", index=False)
        puts_df.to_csv("nifty_puts_data.csv", index=False)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")
