# Databricks notebook source
geolocation_df=spark.read.format('csv').option('header',True).load('/Volumes/olist-container-9pm/landing/files/olist_geolocation_dataset.csv')
geolocation_df.printSchema()
#geolocation_df.display()

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType, BooleanType, FloatType

geolocation_schema = StructType([
    StructField("geolocation_zip_code_prefix", IntegerType(), nullable=True),
    StructField("geolocation_lat", FloatType(), nullable=True),
    StructField("geolocation_lng", FloatType(), nullable=True),
    StructField("geolocation_city", StringType(), nullable=True),
    StructField("geolocation_state", StringType(), nullable=True)
])

geolocation_df=spark.read.format('csv').option('header', True).schema(geolocation_schema).load('/Volumes/olist-container-9pm/landing/files/olist_geolocation_dataset.csv')

geolocation_df.display()

# COMMAND ----------

from pyspark.sql import functions as f

geolocation_df=geolocation_df.withColumn('timestamp',f.current_timestamp())
geolocation_df=geolocation_df.withColumn('source',f.col('_metadata.file_path'))

geolocation_df.display()

# COMMAND ----------

geolocation_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.bronze.olist_geolocation_dataset')
df=spark.read.table('`olist-container-9pm`.bronze.olist_geolocation_dataset')
df.display()