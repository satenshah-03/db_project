# Databricks notebook source
items_df=spark.read.table('`olist-container-9pm`.bronze.olist_order_items_dataset')
items_df.display()

# COMMAND ----------

from pyspark.sql.functions import year, month, dayofmonth, to_date, col

items_df = items_df.withColumn(
    "shipping_limit_date",
    to_date(col("shipping_limit_date"), "yyyy-MM-dd")
)

items_df = items_df.withColumn("Year", year(col("shipping_limit_date"))) \
       .withColumn("Month", month(col("shipping_limit_date"))) \
       .withColumn("Date", dayofmonth(col("shipping_limit_date")))
items_df.display()

# COMMAND ----------

from pyspark.sql import functions as f
items_df=items_df.filter(f.isnotnull(items_df['order_id']))
items_df.display()

# COMMAND ----------

# DBTITLE 1,Write order items to silver
items_df.write.format('delta').mode('overwrite').option('overwriteSchema', 'true').saveAsTable('`olist-container-9pm`.silver.olist_order_items_dataset')
items_df.display()