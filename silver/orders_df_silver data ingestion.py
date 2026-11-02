# Databricks notebook source
orders_df=spark.read.table('`olist-container-9pm`.bronze.olist_orders_dataset')
orders_df.display()

# COMMAND ----------

orders_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.silver.olist_orders_dataset')
orders_df.display()