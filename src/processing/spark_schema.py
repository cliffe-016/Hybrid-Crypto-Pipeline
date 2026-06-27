# The universal Debezium Source and Transaction blocks
SOURCE_BLOCK = """
  {"name": "source", "type": {"type": "record", "name": "Source", "fields": [
    {"name": "version", "type": "string"},
    {"name": "connector", "type": "string"},
    {"name": "name", "type": "string"},
    {"name": "ts_ms", "type": "long"},
    {"name": "snapshot", "type": ["null", "string"], "default": null},
    {"name": "db", "type": "string"},
    {"name": "sequence", "type": ["null", "string"], "default": null},
    {"name": "schema", "type": "string"},
    {"name": "table", "type": "string"},
    {"name": "txId", "type": ["null", "long"], "default": null},
    {"name": "lsn", "type": ["null", "long"], "default": null},
    {"name": "xmin", "type": ["null", "long"], "default": null}
  ]}}
"""

TRANSACTION_BLOCK = """
  {"name": "transaction", "type": ["null", {"type": "record", "name": "ConnectDefault", "fields": [
    {"name": "id", "type": "string"},
    {"name": "total_order", "type": "long"},
    {"name": "data_collection_order", "type": "long"}
  ]}], "default": null}
"""

candlestick_avro = f"""
{{
  "type": "record", "name": "Envelope", "fields": [
    {{ "name": "before", "type": ["null", {{ "type": "record", "name": "Value", "fields": [
          {{"name": "symbol", "type": ["null", "string"], "default": null}},
          {{"name": "open_time", "type": ["null", "long"], "default": null}},
          {{"name": "open", "type": ["null", "string"], "default": null}},
          {{"name": "high", "type": ["null", "string"], "default": null}},
          {{"name": "low", "type": ["null", "string"], "default": null}},
          {{"name": "close", "type": ["null", "string"], "default": null}},
          {{"name": "volume", "type": ["null", "string"], "default": null}}
    ] }}], "default": null }},
    {{ "name": "after", "type": ["null", "Value"], "default": null }},
    {SOURCE_BLOCK},
    {{"name": "op", "type": "string"}},
    {{"name": "ts_ms", "type": ["null", "long"], "default": null}},
    {TRANSACTION_BLOCK}
  ]
}}
"""

orders_avro = f"""
{{
  "type": "record", "name": "Envelope", "fields": [
    {{ "name": "before", "type": ["null", {{ "type": "record", "name": "Value", "fields": [
          {{"name": "symbol", "type": ["null", "string"], "default": null}},
          {{"name": "bid_price", "type": ["null", "string"], "default": null}},
          {{"name": "bid_qty", "type": ["null", "string"], "default": null}},
          {{"name": "ask_price", "type": ["null", "string"], "default": null}},
          {{"name": "ask_qty", "type": ["null", "string"], "default": null}},
          {{"name": "update_id", "type": ["null", "long"], "default": null}}
    ] }}], "default": null }},
    {{ "name": "after", "type": ["null", "Value"], "default": null }},
    {SOURCE_BLOCK},
    {{"name": "op", "type": "string"}},
    {{"name": "ts_ms", "type": ["null", "long"], "default": null}},
    {TRANSACTION_BLOCK}
  ]
}}
"""

tickers_avro = f"""
{{
  "type": "record", "name": "Envelope", "fields": [
    {{ "name": "before", "type": ["null", {{ "type": "record", "name": "Value", "fields": [
          {{"name": "symbol", "type": ["null", "string"], "default": null}},
          {{"name": "price_change", "type": ["null", "string"], "default": null}},
          {{"name": "price_change_percent", "type": ["null", "string"], "default": null}},
          {{"name": "last_price", "type": ["null", "string"], "default": null}},
          {{"name": "volume", "type": ["null", "string"], "default": null}}
    ] }}], "default": null }},
    {{ "name": "after", "type": ["null", "Value"], "default": null }},
    {SOURCE_BLOCK},
    {{"name": "op", "type": "string"}},
    {{"name": "ts_ms", "type": ["null", "long"], "default": null}},
    {TRANSACTION_BLOCK}
  ]
}}
"""

pairs_avro = f"""
{{
  "type": "record", "name": "Envelope", "fields": [
    {{ "name": "before", "type": ["null", {{ "type": "record", "name": "Value", "fields": [
          {{"name": "symbol", "type": ["null", "string"], "default": null}},
          {{"name": "base_asset", "type": ["null", "string"], "default": null}},
          {{"name": "quote_asset", "type": ["null", "string"], "default": null}},
          {{"name": "status", "type": ["null", "string"], "default": null}}
    ] }}], "default": null }},
    {{ "name": "after", "type": ["null", "Value"], "default": null }},
    {SOURCE_BLOCK},
    {{"name": "op", "type": "string"}},
    {{"name": "ts_ms", "type": ["null", "long"], "default": null}},
    {TRANSACTION_BLOCK}
  ]
}}
"""
