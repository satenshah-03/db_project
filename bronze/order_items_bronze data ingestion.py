# Databricks notebook source

items_df=spark.read.format('csv').option('header',True).load('/Volumes/olist-container-9pm/landing/files/olist_order_items_dataset.csv')

items_df.printSchema()
items_df.display()
items_df.columns

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType, BooleanType, FloatType, TimestampType

items_schema = StructType([
    StructField("order_id", StringType(), nullable=True),
    StructField("order_item_id", IntegerType(), nullable=True),
    StructField("product_id", StringType(), nullable=True),
    StructField("seller_id", StringType(), nullable=True),
    StructField("shipping_limit_date", DateType(), nullable=True),
    StructField("price", FloatType(), nullable=True),
    StructField("freight_value", FloatType(), nullable=True)
])

items_df=spark.read.format('csv').option('header', True).schema(items_schema).load('/Volumes/olist-container-9pm/landing/files/olist_order_items_dataset.csv')
items_df.display()

# COMMAND ----------

from pyspark.sql import functions as f

items_df=items_df.withColumn('timestamp',f.current_timestamp())
items_df=items_df.withColumn('source',f.col('_metadata.file_path'))

items_df.display()

# COMMAND ----------

items_df.write.format('delta').mode('overwrite').option('overwriteSchema', 'true').saveAsTable('`olist-container-9pm`.bronze.olist_order_items_dataset')

df=spark.read.table('`olist-container-9pm`.bronze.olist_order_items_dataset')
df.display()