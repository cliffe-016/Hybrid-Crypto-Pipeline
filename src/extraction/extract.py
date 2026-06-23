from src import config
import time
import requests

def extract():
    """Extracts Data from Binance API endpoints"""
    # Initalize an empty dictionary to store the extracted data
    market_data = {}

    # Open a session to keep the connection alive and improve performance
    with requests.Session() as session:
        try:
            # Store the endpoints in a dictionary to avoid overwriting data
            urls = {
                "ticker": config.price_url,
                "trading_pairs": config.trading_pairs_url
                }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }

            # Iterate over the dictionary to extract the data
            for name, url in urls.items():
                response = session.get(url, headers=headers)
                response.raise_for_status() # raise http errors
                market_data[name] = response.json() # store the data in the empty dictionary

            # Get all the symbols from the price ticker data
            symbols = [ticker['symbol'] for ticker in market_data['ticker']]

            # Iterate over the symbols as mandatory parameters for the remaining endpoints
            for symbol in symbols:
                params = {"symbol": symbol}
                ohlc_params = {"symbol": symbol, "interval": "1M"} # interval is also mandatory for ohlc endpoint
        
                order_data = session.get(config.order_book_url, headers=headers, params=params)
                order_data.raise_for_status()

                ohlc_data = session.get(config.ohlc_url, headers=headers, params=ohlc_params)
                ohlc_data.raise_for_status()

                # Convert the data to json and add the data to the main dictionary with the symbol as the key
                market_data[symbol] = {
                    "order_book": order_data.json(),
                    "candlestick": ohlc_data.json()
                    }
                
                # Add a rate limit delay
                time.sleep(0.2)

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            raise
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: {e}")
            raise
        except Exception as e:
            print(f"Unknown Error: {e}")
            raise
        else:
            print("Data Extraction successful")
            return market_data

