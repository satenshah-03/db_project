# Databricks notebook source
customer_df = spark.read.table('`olist-container-9pm`.silver.olist_customers_dataset')
customer_df.display()


# COMMAND ----------

customer_df = customer_df.select( "customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state" )

customer_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Write to Gold

# COMMAND ----------

# DBTITLE 1,Write dim_customer to gold
customer_df.write\
    .format("delta")\
    .mode("overwrite")\
    .saveAsTable("`olist-container-9pm`.gold.dim_customer")