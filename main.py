import ccxt

# Create an instance of the exchange
exchange = ccxt.binance()

# Set the symbol and timeframe
symbol = 'BTC/USDT'
timeframe = '1d'  # Daily timeframe

# Set the number of candles to retrieve
limit = 1000

# Fetch the OHLCV data
ohlcv_data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

# Print the retrieved data
for candle in ohlcv_data:
    timestamp, open_, high, low, close, volume = candle
    print(f"Timestamp: {timestamp}, Open: {open_}, High: {high}, Low: {low}, Close: {close}, Volume: {volume}")
