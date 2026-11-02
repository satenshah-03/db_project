# Databricks notebook source
orders_df = spark.table("`olist-container-9pm`.silver.olist_orders_dataset")
orders_df.display()


# COMMAND ----------

date_df = orders_df.select( 'order_purchase_timestamp'  )
date_df = date_df.dropDuplicates(subset = ['order_purchase_timestamp'])
date_df.display()

# COMMAND ----------

from pyspark.sql import functions as f

date_df = date_df \
    .withColumn("day", f.dayofmonth("order_purchase_timestamp")) \
    .withColumn("month", f.month("order_purchase_timestamp")) \
    .withColumn("month_name", f.date_format("order_purchase_timestamp", "MMMM")) \
    .withColumn("quarter", f.quarter("order_purchase_timestamp")) \
    .withColumn("year", f.year("order_purchase_timestamp")) \
    .withColumn("weekday", f.date_format("order_purchase_timestamp", "EEEE"))

date_df.display()


# COMMAND ----------

date_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option('overwriteSchema', 'true')\
    .saveAsTable("`olist-container-9pm`.gold.dim_date")
