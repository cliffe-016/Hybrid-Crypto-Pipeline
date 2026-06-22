CREATE KEYSPACE IF NOT EXISTS binance 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE binance;

CREATE TABLE candlestick (
    symbol text,
    window_start timestamp,
    avg_minute_price float,
    total_minute_volume float,
    price_stddev float,
    max_spread float,
    is_anomaly boolean,
    PRIMARY KEY ((symbol), window_start)
) WITH CLUSTERING ORDER BY (window_start DESC);

CREATE TABLE IF NOT EXISTS order_books (
    symbol text,
    lastUpdateId bigint,
    bids text,
    asks text,
    PRIMARY KEY ((symbol), lastUpdateId)
) WITH CLUSTERING ORDER BY (lastUpdateId DESC);


CREATE TABLE IF NOT EXISTS tickers (
    symbol text PRIMARY KEY,
    priceChange text,
    lastPrice text,
    volume text
);


CREATE TABLE IF NOT EXISTS trading_pairs (
    symbol text PRIMARY KEY,
    baseAsset text,
    quoteAsset text,
    status text
);
