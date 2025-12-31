# Databricks notebook source
from pyspark.sql.functions import col, to_date, desc, row_number
from pyspark.sql.window import Window

df = spark.read.table("paystream.bronze_transactions")

win = Window.partitionBy("transaction_id").orderBy(desc("ingest_timestamp"))
df = df.withColumn("r", row_number().over(win)).filter("r=1").drop("r")

df = df.select(
    "transaction_id",
    to_date("timestamp").alias("trx_date"),
    col("merchant_id").cast("long"),
    (col("amount")*100).cast("long").alias("amount_cents"),
    "currency",
    "proc_code",
    "response_code"
)

df.write.format("delta").mode("overwrite").saveAsTable("paystream.silver_transactions")
