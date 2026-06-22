from spark_utils import spark_session
from pyspark.sql.functions import *
from kafka_utils import read_kafka_topic
import spark_schema

spark = spark_session()

# Ingest the streams
raw_candlesstick = read_kafka_topic("binance_stream.public.candlestick_data")
raw_orders = read_kafka_topic("binance_stream.public.order_books")
raw_tickers = read_kafka_topic("binance_stream.public.tickers")
raw_pairs = read_kafka_topic("binance_stream.public.trading_pairs")

# Enrich the cnadlestick data
enriched_candlestick = raw_candlestick \
    .selectExpr("CAST(value AS STRING)") \ #cast kafka bytes to string
    .select(from_json(col("value"), schemas.wrap_debezium(schemas.candlestick_schema)).alias("data")).select("data.payload.after.*") \ #apply schema to the json data and convert to spark dataframe
    .withColumn("price", col("close").cast("float")) \
    .withColumn("price_high", col("high").cast("float")) \
    .withColumn("price_low", col("low").cast("float")) \
    .withColumn("trade_volume", col("volume").cast("float")) \
    .withColumn("timestamp", to_timestamp(col("open_time") / 1000)) \ #convert ms timestamp to seconds
    .withWatermark("timestamp", "2 minutes") \ #2 min memory window
    .groupBy(window(col("timestamp"), "1 minute"), col("symbol")) \ #bin event time by 60s
    .agg(
        avg("price").alias("avg_minute_price"),
        sum("trade_volume").alias("total_volume_min"),
        stddev("price").alias("price_stddev"),
        (max("high_price") - min("low_price")).alias("max_spread")
        ) 

# Flatten the window struct so Cassandra can read it
candlestick_df = enriched_candles \
    .withColumn("window_start", col("window.start")) \
    .drop("window")

# Transform the remaining data
clean_orders = raw_books \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schemas.wrap_debezium(schemas.order_book_schema)).alias("data")).select("data.payload.after.*")

clean_tickers = raw_tickers \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schemas.wrap_debezium(schemas.ticker_schema)).alias("data")).select("data.payload.after.*")

clean_pairs = raw_pairs \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schemas.wrap_debezium(schemas.trading_pairs_schema)).alias("data")).select("data.payload.after.*")

# Execute the streams 
query_candles = candlestick_df.writeStream.outputMode("update") \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "binance") \
    .option("table", "candlestick") \
    .option("spark.cassandra.connection.host", "cassandra") \
    .option("spark.cassandra.connection.port", "9042") \
    .option("checkpointLocation", "/tmp/checkpoints/candlestick") \
    .start()

query_orders = clean_orders.writeStream.outputMode("append") \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "binance") \
    .option("table", "order_books") \
    .option("spark.cassandra.connection.host", "cassandra") \
    .option("spark.cassandra.connection.port", "9042") \
    .option("checkpointLocation", "/tmp/checkpoints/order_books") \
    .start()

query_tickers = clean_tickers.writeStream.outputMode("append")
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "binance") \
    .option("table", "tickers") \
    .option("spark.cassandra.connection.host", "cassandra") \
    .option("spark.cassandra.connection.port", "9042") \
    .option("checkpointLocation", "/tmp/checkpoints/tickers") \
    .start()

query_pairs = clean_pairs.writeStream.outputMode("append")
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "binance") \
    .option("table", "trading_pairs") \
    .option("spark.cassandra.connection.host", "cassandra") \
    .option("spark.cassandra.connection.port", "9042") \
    .option("checkpointLocation", "/tmp/checkpoints/trading_pairs") \
    .start()

spark.streams.awaitAnyTermination()
