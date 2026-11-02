# Databricks notebook source

orders_df=spark.read.format('csv').option('header',True).load('/Volumes/olist-container-9pm/landing/files/olist_orders_dataset.csv')

orders_df.printSchema()
orders_df.display()
orders_df.columns

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType, BooleanType, FloatType, TimestampType

orders_schema = StructType([
    StructField("order_id", StringType(), nullable=True),
    StructField("customer_id", StringType(), nullable=True),
    StructField("order_status", StringType(), nullable=True),
    StructField("order_purchase_timestamp", TimestampType(), nullable=True),
    StructField("order_approved_at", TimestampType(), nullable=True),
    StructField("order_delivered_carrier_date", TimestampType(), nullable=True),
    StructField("order_delivered_customer_date", TimestampType(), nullable=True),
    StructField("order_estimated_delivery_date", TimestampType(), nullable=True)
])

orders_df=spark.read.format('csv').option('header', True).schema(orders_schema).load('/Volumes/olist-container-9pm/landing/files/olist_orders_dataset.csv')
orders_df.display()

# COMMAND ----------

from pyspark.sql import functions as f

orders_df=orders_df.withColumn('timestamp',f.current_timestamp())
orders_df=orders_df.withColumn('source',f.col('_metadata.file_path'))

orders_df.display()

# COMMAND ----------

orders_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.bronze.olist_orders_dataset')

df=spark.read.table('`olist-container-9pm`.bronze.olist_orders_dataset')
df.display()