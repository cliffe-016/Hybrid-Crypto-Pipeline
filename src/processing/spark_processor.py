from src.utils.spark_utils import spark_session
from pyspark.sql.functions import *
from pyspark.sql.avro.functions import from_avro
from src.utils.kafka_utils import read_kafka_topic
import src.processing.spark_schema 

spark = spark_session()

# Ingest the streams
raw_candlestick = read_kafka_topic("binance_server.public.candlestick_data")
raw_orders = read_kafka_topic("binance_server.public.order_books")
raw_tickers = read_kafka_topic("binance_server.public.tickers")
raw_pairs = read_kafka_topic("binance_server.public.trading_pairs")

# Slice off the 5-byte Confluent Schema Registry header for all streams
clean_avro_bytes = expr("substring(value, 6, length(value)-5)")

# Enrich the cnadlestick data
enriched_candlestick = raw_candlestick \
    .withColumn("avro_data", from_avro(clean_avro_bytes, candlestick_avro)) \
    .select("avro_data.after.*") \
    .withColumn("price", col("close").cast("float")) \
    .withColumn("price_high", col("high").cast("float")) \
    .withColumn("price_low", col("low").cast("float")) \
    .withColumn("trade_volume", col("volume").cast("float")) \
    .withColumn("timestamp", to_timestamp(col("open_time") / 1000)) \
    .withWatermark("timestamp", "2 minutes") \
    .groupBy(window(col("timestamp"), "1 minute"), col("symbol")) \
    .agg(
        avg("price").alias("avg_minute_price"),
        sum("trade_volume").alias("total_volume_min"),
        stddev("price").alias("price_stddev"),
        (max("price_high") - min("price_low")).alias("max_spread")
        ) 

# Flatten the window struct so Cassandra can read it
candlestick_df = enriched_candlestick \
    .withColumn("window_start", col("window.start")) \
    .drop("window")

# Deserialze and flatten the remaining data
clean_orders = raw_orders \
    .withColumn("avro_data", from_avro(clean_avro_bytes, orders_avro)) \
    .select("avro_data.after.*")

clean_tickers = raw_tickers \
    .withColumn("avro_data", from_avro(clean_avro_bytes, tickers_avro)) \
    .select("avro_data.after.*")

clean_pairs = raw_pairs \
    .withColumn("avro_data", from_avro(clean_avro_bytes, pairs_avro)) \
    .select("avro_data.after.*")

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

query_tickers = clean_tickers.writeStream.outputMode("append") \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "binance") \
    .option("table", "tickers") \
    .option("spark.cassandra.connection.host", "cassandra") \
    .option("spark.cassandra.connection.port", "9042") \
    .option("checkpointLocation", "/tmp/checkpoints/tickers") \
    .start()

query_pairs = clean_pairs.writeStream.outputMode("append") \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "binance") \
    .option("table", "trading_pairs") \
    .option("spark.cassandra.connection.host", "cassandra") \
    .option("spark.cassandra.connection.port", "9042") \
    .option("checkpointLocation", "/tmp/checkpoints/trading_pairs") \
    .start()

spark.streams.awaitAnyTermination()
