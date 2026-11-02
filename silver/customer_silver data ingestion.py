# Databricks notebook source
customer_df=spark.read.table('`olist-container-9pm`.bronze.olist_customers_dataset')
customer_df.display()

# COMMAND ----------

from pyspark.sql import functions as f
customer_df=customer_df.withColumn('customer_city',f.lower(customer_df['customer_city']))
customer_df.display()

# COMMAND ----------

customer_df=customer_df.filter(f.isnotnull(customer_df['customer_id']))
customer_df.display()

# COMMAND ----------

customer_df=customer_df.dropDuplicates(['customer_id'])
customer_df.display()

# COMMAND ----------

customer_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.silver.olist_customers_dataset')
customer_df.display()