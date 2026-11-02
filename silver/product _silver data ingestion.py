# Databricks notebook source
product_df=spark.read.table('`olist-container-9pm`.bronze.olist_products_dataset')
product_df.display()

# COMMAND ----------

from pyspark.sql import functions as f
product_df=product_df.withColumn('product_category_name',f.lower(product_df['product_category_name']))
product_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Check product id Null value

# COMMAND ----------

#product_df.filter(f.isnull(product_df['product_id'])).display()
product_df=product_df.filter(f.isnotnull(product_df['product_id']))
product_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Check duplicate value

# COMMAND ----------

product_df=product_df.dropDuplicates(['product_id'])
product_df.display()
#product_df.write.mode('overwrite').saveAsTable('`olist-container-9pm`.silver.olist_products_dataset')

# COMMAND ----------

# DBTITLE 1,Filter out non-positive product dimensions
product_df=product_df.filter(product_df['product_weight_g']>0)
product_df=product_df.filter(product_df['product_length_cm']>0)
product_df=product_df.filter(product_df['product_height_cm']>0)
product_df=product_df.filter(product_df['product_width_cm']>0)
product_df.display()

# COMMAND ----------

product_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.silver.olist_products_dataset')
product_df.display()