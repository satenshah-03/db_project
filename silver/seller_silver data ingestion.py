# Databricks notebook source
seller_df=spark.read.table('`olist-container-9pm`.bronze.olist_sellers_dataset')
seller_df.display()

# COMMAND ----------

from pyspark.sql import functions as f
seller_df=seller_df.filter(f.isnotnull(seller_df['seller_id:']))
seller_df=seller_df.dropDuplicates(['seller_id:'])
seller_df=seller_df.withColumn('seller_city',f.lower(seller_df['seller_city']))
seller_df=seller_df.withColumn('seller_state',f.lower(seller_df['seller_state']))
seller_df.display()

# COMMAND ----------

seller_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.silver.olist_sellers_dataset')
seller_df.display()