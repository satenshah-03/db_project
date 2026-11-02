# Databricks notebook source
geo_df = spark.table("`olist-container-9pm`.silver.olist_geolocation_dataset")
geo_df.display()
geo_df.count()

# COMMAND ----------

from pyspark.sql.functions import avg, first

geo_df = geo_df.groupBy(
    "geolocation_zip_code_prefix"
).agg(
    avg("geolocation_lat").alias("latitude"),
    avg("geolocation_lng").alias("longitude"),
    first("geolocation_city", ignorenulls=True).alias("city"),
    first("geolocation_state", ignorenulls=True).alias("state")
)

geo_df.display()
geo_df.count()

# COMMAND ----------

geo_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("`olist-container-9pm`.gold.dim_location")