# Databricks notebook source
from pyspark.sql.functions import col, sum, when

df = spark.read.table("paystream.silver_transactions")

settlement = (df.filter(col("response_code")=="00")
  .groupBy("merchant_id","currency","trx_date")
  .agg(sum(
        when(col("proc_code")=="000000",col("amount_cents"))
       .when(col("proc_code")=="200000",col("amount_cents")*-1)
       .otherwise(0)
  ).alias("net_cents"))
)

settlement.write.format("delta").mode("overwrite").saveAsTable("paystream.gold_daily_settlement")
