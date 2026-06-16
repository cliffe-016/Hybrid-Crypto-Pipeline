import config
import json
import requests

def extract():
    """Extracts Data from Binance's API endpoints"""
    try:
        # Initalize an empty dictionary to store the extracted data
        market_data = {}

        # Store the endpoints in a dictionary to avoid overwriting data
        urls = {
            "ticker": config.price_url,
            "trading_pairs": config.trading_pairs_url
            }

        # Iterate over the dictionary to extract the data
        for name, url in urls.items():
            repsonse = requests.get(url)
            market_data[name] = response.json() # store the data in the empty dictionary

        # Get all the symbols from the price ticker data
        symbols = [ticker['symbol'] for ticker in market_data['ticker']]

        # Iterate over the symbols as mandatory parameters for the remaining endpoints
        for symbol in symbols:
            params = {"symbol": symbol}
            ohlc_params = {"symbol": symbol, "interval": "1M"} # interval is also mandatory for ohlc endpoint
        
            order_data = requests.get(config.order_book_url, params=params)
            ohlc_data = requests.get(config.ohlc_url, params=ohlc_params)

            # Convert the data to json and add the data to the main dictionary with the symbol as the key
            market_data[symbol] = {
                "order_book": order_data.json(),
                "candlestick": ohlc_url,json()
                }

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    else:
        print("Data Extraction successful")
        return market_data

