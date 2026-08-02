import os
import time
import logging
import yfinance as yf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when

logger = logging.getLogger("stock_sense_spark")

def execute_distributed_etl(ticker: str, exchange: str, s3_bucket: str) -> float:
    start_time = time.time()
    
    aws_key = os.environ.get("AWS_ACCESS_KEY_ID", "mock")
    aws_secret = os.environ.get("AWS_SECRET_ACCESS_KEY", "mock")
    bucket_target = s3_bucket if s3_bucket else os.environ.get("AWS_STORAGE_BUCKET_NAME", "fallback-lake")
    
    suffix = ".NS" if exchange.upper() == "NSE" else ".BO"
    yf_symbol = f"{ticker.upper()}{suffix}"
    
    ticker_obj = yf.Ticker(yf_symbol)
    df_history = ticker_obj.history(period="1mo", interval="1d").reset_index()
    
    if df_history.empty:
        raise ValueError(f"No historical records found for {yf_symbol}")
        
    df_history['Date'] = df_history['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    spark = SparkSession.builder \
        .appName(f"StockSense-CloudETL-{ticker}") \
        .master("local[*]") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
        .config("spark.hadoop.fs.s3a.access.key", aws_key) \
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret) \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.sql.parquet.compression.codec", "snappy") \
        .getOrCreate()
        
    try:
        spark_df = spark.createDataFrame(df_history)
        
        processed_df = spark_df.withColumn("Ticker", lit(ticker.upper())) \
            .withColumn("Exchange", lit(exchange.upper())) \
            .withColumn("LTP", when(col("Adj Close").isNotNull(), col("Adj Close")).otherwise(col("Close"))) \
            .withColumn("Daily_Spread", col("High") - col("Low")) \
            .filter(col("Volume") > 0) \
            .dropDuplicates(["Date", "Ticker"])
            
        cloud_s3a_path = f"s3a://{bucket_target}/curated/historical_snapshots/ticker={ticker.lower()}/"
        
        processed_df.write \
            .mode("overwrite") \
            .partitionBy("Exchange") \
            .parquet(cloud_s3a_path)
            
    finally:
        spark.stop()
        
    return round(time.time() - start_time, 2)

