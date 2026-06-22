from pyspark.sql import SparkSession

def spark_session(app_name="BinanceCDCStream"):
    spark = SparkSession.builder.appName(app_name_.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark
