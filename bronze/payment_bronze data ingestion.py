# Databricks notebook source
payment_df=spark.read.format('csv').option('header',True).load('/Volumes/olist-container-9pm/landing/files/olist_order_payments_dataset.csv')
payment_df.printSchema()
payment_df.display(5)

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType, BooleanType, FloatType

payment_schema = StructType([
    StructField("order_id", StringType(), nullable=True),
    StructField("payment_sequential", IntegerType(), nullable=True),
    StructField("payment_type", StringType(), nullable=True),
    StructField("payment_installments", IntegerType(), nullable=True),
    StructField("payment_value", FloatType(), nullable=True)
])

payment_df=spark.read.format('csv').option('header', True).schema(payment_schema).load('/Volumes/olist-container-9pm/landing/files/olist_order_payments_dataset.csv')

payment_df.display()

# COMMAND ----------

from pyspark.sql import functions as f

payment_df=payment_df.withColumn('timestamp',f.current_timestamp())
payment_df=payment_df.withColumn('source',f.col('_metadata.file_path'))

payment_df.display()

# COMMAND ----------

payment_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.bronze.olist_payment_dataset')
df=spark.read.table('`olist-container-9pm`.bronze.olist_payment_dataset')
df.display()