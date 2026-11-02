# Databricks notebook source
reviews_df=spark.read.format('csv').option('header',True).load('/Volumes/olist-container-9pm/landing/files/olist_order_reviews_dataset.csv')
reviews_df.printSchema()
reviews_df.display()


# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType, BooleanType, FloatType, TimestampType

reviews_schema = StructType([
    StructField("review_id", StringType(), nullable=True),
    StructField("order_id", StringType(), nullable=True),
    StructField("review_score", IntegerType(), nullable=True),
    StructField("review_comment_title", StringType(), nullable=True),
    StructField("review_comment_message", StringType(), nullable=True),
    StructField("review_creation_date", TimestampType(), nullable=True),
    StructField("review_answer_timestamp", TimestampType(), nullable=True)
])

reviews_df=spark.read.format('csv').option('header', True).schema(reviews_schema).load('/Volumes/olist-container-9pm/landing/files/olist_order_reviews_dataset.csv')

reviews_df.display()

# COMMAND ----------

from pyspark.sql import functions as f

reviews_df=reviews_df.withColumn('timestamp',f.current_timestamp())
reviews_df=reviews_df.withColumn('source',f.col('_metadata.file_path'))

reviews_df.display()

# COMMAND ----------

# DBTITLE 1,Write reviews to bronze Delta table
reviews_df.write.format('delta').mode('overwrite').option('overwriteSchema', 'true').saveAsTable('`olist-container-9pm`.bronze.olist_reviews_dataset')
df=spark.read.table('`olist-container-9pm`.bronze.olist_reviews_dataset')
df.display()