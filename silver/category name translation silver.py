# Databricks notebook source
translation_df=spark.read.table('`olist-container-9pm`.bronze.product_category_name_translation')
translation_df.display()

# COMMAND ----------

translation_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.silver.product_category_name_translation')
translation_df.display()