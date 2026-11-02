# Databricks notebook source
customer_df=spark.read.format('csv').option('header',True).load('/Volumes/olist-container-9pm/landing/files/olist_customers_dataset.csv')
customer_df.printSchema()

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType, BooleanType, FloatType

customer_schema = StructType([
    StructField("customer_id", StringType(), nullable=True),
    StructField("customer_unique_id", StringType(), nullable=True),
    StructField("customer_zip_code_prefix", IntegerType(), nullable=True),
    StructField("customer_city", StringType(), nullable=True),
    StructField("customer_state", StringType(), nullable=True)
])

customer_df=spark.read.format('csv').option('header', True).schema(customer_schema).load('/Volumes/olist-container-9pm/landing/files/olist_customers_dataset.csv')

customer_df.display()

# COMMAND ----------

from pyspark.sql import functions as f

customer_df=customer_df.withColumn('timestamp',f.current_timestamp())
customer_df=customer_df.withColumn('source',f.col('_metadata.file_path'))

customer_df.display()

# COMMAND ----------

customer_df = customer_df.withColumn('customer_zip_code_prefix', customer_df['customer_zip_code_prefix'].cast('string'))
customer_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.bronze.olist_customers_dataset')
df=spark.read.table('`olist-container-9pm`.bronze.olist_customers_dataset')
df.display()