import os
from dotenv import load_dotenv

load_dotenv()

# Define the api endpoints
base_url = os.getenv("BASE_URL")

price_url = base_url + os.getenv("PRICE")
trading_pairs_url = base_url + os.getenv("TRADING_PAIRS")
order_book_url = base_url + os.getenv("ORDER_BOOK")
ohlc_url = base_url + os.getenv("OHLC")



