from pyspark.sql import SparkSession

def spark_session(app_name="BinanceStream"):
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark
