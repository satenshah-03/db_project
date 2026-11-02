# Databricks notebook source
geolocation_df=spark.read.table('`olist-container-9pm`.bronze.olist_geolocation_dataset')
geolocation_df.display()

# COMMAND ----------

geolocation_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.silver.olist_geolocation_dataset')
geolocation_df.display()