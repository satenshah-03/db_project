# Databricks notebook source
# MAGIC %md
# MAGIC Loading data and schema

# COMMAND ----------

product_df=spark.read.format('csv').option('header',True).load('/Volumes/olist-container-9pm/landing/files/olist_products_dataset.csv')

product_df.printSchema()
product_df.display()
product_df.columns

# COMMAND ----------

# MAGIC %md
# MAGIC Schema enforcement

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType, BooleanType, FloatType, TimestampType

product_schema = StructType([
    StructField("product_id", StringType(), nullable=True),
    StructField("product_category_name", StringType(), nullable=True),
    StructField("product_name_lenght", IntegerType(), nullable=True),
    StructField("product_description_lenght", IntegerType(), nullable=True),
    StructField("product_photos_qty", IntegerType(), nullable=True),
    StructField("product_weight_g", IntegerType(), nullable=True),
    StructField("product_length_cm", IntegerType(), nullable=True),
    StructField("product_height_cm", IntegerType(), nullable=True),
    StructField("product_width_cm", IntegerType(), nullable=True)
])

product_df=spark.read.format('csv').option('header', True).schema(product_schema).load('/Volumes/olist-container-9pm/landing/files/olist_products_dataset.csv')
product_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Rename column

# COMMAND ----------

product_df=product_df=spark.read.format('csv').option('header', True).schema(product_schema).load('/Volumes/olist-container-9pm/landing/files/olist_products_dataset.csv')
prduct_df=product_df.withColumnRenamed('product_name_lenght','product_name_length')
prduct_df=product_df.withColumnRenamed('product_description_lenght','product_description_length')

#product_df.display()


# COMMAND ----------

# MAGIC %md
# MAGIC Adding time stamp and data source

# COMMAND ----------

from pyspark.sql import functions as f

product_df=product_df.withColumn('timestamp',f.current_timestamp())
product_df=product_df.withColumn('source',f.col('_metadata.file_path'))

#product_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Sending data to bronze & overwrite or append the data

# COMMAND ----------

product_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.bronze.olist_products_dataset')

df=spark.read.table('`olist-container-9pm`.bronze.olist_products_dataset')
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Same code in sql

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from `olist-container-9pm`.bronze.olist_products_dataset