# Databricks notebook source
translation_df=spark.read.format('csv').option('header',True).load('/Volumes/olist-container-9pm/landing/files/product_category_name_translation.csv')

translation_df.printSchema()
translation_df.display()
translation_df.columns

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType, BooleanType, FloatType, TimestampType

translation_schema = StructType([
    StructField("product_category_name", StringType(), nullable=True),
    StructField("product_category_name_english", StringType(), nullable=True)
])

translation_df=spark.read.format('csv').option('header', True).schema(translation_schema).load('/Volumes/olist-container-9pm/landing/files/product_category_name_translation.csv')
translation_df.display()

# COMMAND ----------

from pyspark.sql import functions as f

translation_df=translation_df.withColumn('timestamp',f.current_timestamp())
translation_df=translation_df.withColumn('source',f.col('_metadata.file_path'))

translation_df.display()

# COMMAND ----------

translation_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.bronze.product_category_name_translation')

df=spark.read.table('`olist-container-9pm`.bronze.product_category_name_translation')
df.display()