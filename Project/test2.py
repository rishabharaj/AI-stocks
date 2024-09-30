from dhanhq import marketfeed

# Replace with your Dhan Client ID and Access Token
client_id = "1104332462"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI3MDMyMzM3LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDMzMjQ2MiJ9.0xY339lMebHdHq6fdpzjzcFrVPzVuO1miGB5HiNQlGvfcnG4RJ-cqPmhnQDtxMGY_LCIxCo56TESBRtLKjL69g"

# Instrument for subscription (e.g., HDFC Bank)
instruments = [
    (marketfeed.NSE, "1333", marketfeed.Ticker)  # 1333 is the security ID for HDFC Bank on NSE
]

# Initialize the DhanFeed class
data = marketfeed.DhanFeed(client_id, access_token, instruments)

# Start fetching live data
try:
    while True:
        data.run_forever()  # Keep connection alive
        response = data.get_data()  # Fetch real-time data
        if response:
            print(response)  # Print the live data for testing
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    data.disconnect()  # Disconnect the feed after use
