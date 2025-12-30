from pyspark.sql.functions import current_timestamp

schema_path = "/mnt/paystream/schema"
checkpoint = "/mnt/paystream/chk_bronze"

df = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format","json")
  .option("cloudFiles.schemaLocation",schema_path)
  .load("/mnt/paystream/landing"))

df = df.withColumn("ingest_time", current_timestamp())

(df.writeStream
 .format("delta")
 .option("checkpointLocation",checkpoint)
 .trigger(availableNow=True)
 .table("paystream.bronze_transactions"))
