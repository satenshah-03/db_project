# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS olist_ext_loc_9pm
# MAGIC URL "abfss://olist-container-9pm@olistadls9pm2.dfs.core.windows.net/"
# MAGIC WITH (STORAGE CREDENTIAL olist_storage_credential_9pm
# MAGIC );

# COMMAND ----------

# DBTITLE 1,Cell 2
# MAGIC %fs ls abfss://olist-container-9pm@olistadls9pm2.dfs.core.windows.net

# COMMAND ----------

# MAGIC %fs ls abfss://olist-container-9pm@olistadls9pm2.dfs.core.windows.net/landing/

# COMMAND ----------

df=spark.read.csv('abfss://olist-container-9pm@olistadls9pm2.dfs.core.windows.net/landing/olist_customers_dataset.csv',inferSchema=True,header=True)
df.display()