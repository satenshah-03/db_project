# Databricks notebook source
sellers_df=spark.read.format('csv').option('header',True).load('/Volumes/olist-container-9pm/landing/files/olist_sellers_dataset.csv')

sellers_df.printSchema()
sellers_df.display()
sellers_df.columns

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType, BooleanType, FloatType, TimestampType

sellers_schema = StructType([
    StructField("seller_id:", StringType(), nullable=True),
    StructField("seller_zip_code_prefix", IntegerType(), nullable=True),
    StructField("seller_city", StringType(), nullable=True),
    StructField("seller_state", StringType(), nullable=True)
])

sellers_df=spark.read.format('csv').option('header', True).schema(sellers_schema).load('/Volumes/olist-container-9pm/landing/files/olist_sellers_dataset.csv')
sellers_df.display()

# COMMAND ----------

from pyspark.sql import functions as f

sellers_df=sellers_df.withColumn('timestamp',f.current_timestamp())
osellers_df=sellers_df.withColumn('source',f.col('_metadata.file_path'))

sellers_df.display()

# COMMAND ----------

sellers_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.bronze.olist_sellers_dataset')

df=spark.read.table('`olist-container-9pm`.bronze.olist_sellers_dataset')
df.display()