from pyspark.sql import Row
from pyspark.sql.functions import col, sum, when

def test_financial_correctness(spark):
    df = spark.createDataFrame([
        Row(proc_code="000000",response_code="00",amount_cents=1000),
        Row(proc_code="200000",response_code="00",amount_cents=500),
        Row(proc_code="000000",response_code="05",amount_cents=9999),
    ])

    total = (df.filter(col("response_code")=="00")
       .agg(sum(
           when(col("proc_code")=="000000",col("amount_cents"))
          .when(col("proc_code")=="200000",col("amount_cents")*-1)
          .otherwise(0)
       ).alias("net")).collect()[0]["net"])

    assert total == 500
