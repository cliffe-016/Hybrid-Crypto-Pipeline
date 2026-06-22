from pyspark.sql.types import *

def wrap_debezium(schema):
    """Wraps a schema in the Debezium payload envelope"""
    return StructType([
                StructField("payload", StructType([
                    StructField("after", schema, True)
                    ]), True)
                ])

candlestick_schema = StructType([
    StructField("open_time", LongType(), True),
    StructField("open", StringType(), True),
    StructField("high", StringType(), True),
    StructField("low", StringType(), True),
    StructField("close", StringType(), True),
    StructField("volume", StringType(), True),
    StructField("symbol", StringType(), True)
])

order_book_schema = StructType([
    StructField("lastUpdateId", LongType(), True),
    StructField("bids", StringType(), True), 
    StructField("asks", StringType(), True),
    StructField("symbol", StringType(), True)
])

ticker_schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("priceChange", StringType(), True),
    StructField("lastPrice", StringType(), True),
    StructField("volume", StringType(), True)
])

trading_pairs_schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("baseAsset", StringType(), True),
    StructField("quoteAsset", StringType(), True),
    StructField("status", StringType(), True)
])
