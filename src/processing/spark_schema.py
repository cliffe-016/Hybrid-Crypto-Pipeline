candlestick_avro = """
{
  "type": "record", "name": "Envelope", "fields": [
    { "name": "after", "type": ["null", { "type": "record", "name": "Value", "fields": [
          {"name": "symbol", "type": ["null", "string"], "default": null},
          {"name": "open_time", "type": ["null", "long"], "default": null},
          {"name": "open", "type": ["null", "string"], "default": null},
          {"name": "high", "type": ["null", "string"], "default": null},
          {"name": "low", "type": ["null", "string"], "default": null},
          {"name": "close", "type": ["null", "string"], "default": null},
          {"name": "volume", "type": ["null", "string"], "default": null}
        ] }], "default": null }
  ]
}
"""

orders_avro = """
{
  "type": "record", "name": "Envelope", "fields": [
    { "name": "after", "type": ["null", { "type": "record", "name": "Value", "fields": [
          {"name": "symbol", "type": ["null", "string"], "default": null},
          {"name": "bid_price", "type": ["null", "string"], "default": null},
          {"name": "bid_qty", "type": ["null", "string"], "default": null},
          {"name": "ask_price", "type": ["null", "string"], "default": null},
          {"name": "ask_qty", "type": ["null", "string"], "default": null},
          {"name": "update_id", "type": ["null", "long"], "default": null}
        ] }], "default": null }
  ]
}
"""

tickers_avro = """
{
  "type": "record", "name": "Envelope", "fields": [
    { "name": "after", "type": ["null", { "type": "record", "name": "Value", "fields": [
          {"name": "symbol", "type": ["null", "string"], "default": null},
          {"name": "price_change", "type": ["null", "string"], "default": null},
          {"name": "price_change_percent", "type": ["null", "string"], "default": null},
          {"name": "last_price", "type": ["null", "string"], "default": null},
          {"name": "volume", "type": ["null", "string"], "default": null}
        ] }], "default": null }
  ]
}
"""

pairs_avro = """
{
  "type": "record", "name": "Envelope", "fields": [
    { "name": "after", "type": ["null", { "type": "record", "name": "Value", "fields": [
          {"name": "symbol", "type": ["null", "string"], "default": null},
          {"name": "base_asset", "type": ["null", "string"], "default": null},
          {"name": "quote_asset", "type": ["null", "string"], "default": null},
          {"name": "status", "type": ["null", "string"], "default": null}
        ] }], "default": null }
  ]
}
"""
