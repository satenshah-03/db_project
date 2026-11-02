# Databricks notebook source
# MAGIC %md
# MAGIC Create Catalog, Schema, Volume

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW CATALOGS;

# COMMAND ----------

# MAGIC %md
# MAGIC Create catalog

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG  IF NOT EXISTS  `olist-container-9pm`
# MAGIC     MANAGED LOCATION 'abfss://olist-container-9pm@olistadls9pm2.dfs.core.windows.net' 
# MAGIC COMMENT '<comment>' ;

# COMMAND ----------

# MAGIC %md
# MAGIC Create Schema/Database

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA  IF NOT EXISTS  `olist-container-9pm`.landing;
# MAGIC CREATE SCHEMA  IF NOT EXISTS  `olist-container-9pm`.bronze
# MAGIC       MANAGED LOCATION 'abfss://olist-container-9pm@olistadls9pm2.dfs.core.windows.net/bronze';
# MAGIC CREATE SCHEMA IF NOT EXISTS  `olist-container-9pm`.silver
# MAGIC       MANAGED LOCATION 'abfss://olist-container-9pm@olistadls9pm2.dfs.core.windows.net/silver';
# MAGIC CREATE SCHEMA  IF NOT EXISTS  `olist-container-9pm`.gold
# MAGIC       MANAGED LOCATION 'abfss://olist-container-9pm@olistadls9pm2.dfs.core.windows.net/gold';

# COMMAND ----------

# MAGIC %sql
# MAGIC     show schemas;

# COMMAND ----------

# MAGIC %sql
# MAGIC  select current_catalog();

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC use catalog `olist-container-9pm`;

# COMMAND ----------

# MAGIC %sql
# MAGIC  select current_catalog();

# COMMAND ----------

# MAGIC %sql
# MAGIC     show schemas;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC use catalog `olist-container-9pm`;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL VOLUME IF NOT EXISTS `olist-container-9pm`.landing.files
# MAGIC     LOCATION 'abfss://olist-container-9pm@olistadls9pm2.dfs.core.windows.net/landing';

# COMMAND ----------

df=spark.read.csv('/Volumes/olist-container-9pm/landing/files/olist_customers_dataset.csv',header=True)
df.display()

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog `olist-container-9pm`;
# MAGIC show schemas;

# COMMAND ----------

# MAGIC %fs ls /Volumes/olist-container-9pm/landing/files

# COMMAND ----------

