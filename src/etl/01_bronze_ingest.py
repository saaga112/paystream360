# Databricks notebook source
# File: src/etl/01_bronze_ingest.py
from pyspark.sql.functions import current_timestamp

# SENIOR CONFIGURATION: Use the direct ABFSS path
# This requires Unity Catalog External Location access (see step 3 below)
storage_account = "paystreamstore12345"
container = "datalake"
base_path = f"abfss://{container}@{storage_account}.dfs.core.windows.net"

# Define paths relative to the root container
schema_path = f"{base_path}/schema/bronze_autoloader"
checkpoint_path = f"{base_path}/checkpoints/bronze"
landing_path = f"{base_path}/landing"

# Read Stream using Auto Loader (CloudFiles)
df = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", schema_path)
  .option("cloudFiles.inferColumnTypes", "true") 
  .load(landing_path))

# Add Audit Columns
df_enriched = df.withColumn("ingest_timestamp", current_timestamp())

# Write Stream to Delta
(df_enriched.writeStream
 .format("delta")
 .option("checkpointLocation", checkpoint_path)
 .trigger(availableNow=True) # Batch mode: Process all available data then stop
 .table("paystream.bronze_transactions"))