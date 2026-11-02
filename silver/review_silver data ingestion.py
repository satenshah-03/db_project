# Databricks notebook source
review_df=spark.read.table('`olist-container-9pm`.bronze.olist_reviews_dataset')
review_df.display()

# COMMAND ----------

review_df=review_df.dropDuplicates(['review_id'])
review_df.display()

# COMMAND ----------

review_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.silver.olist_reviews_dataset')
review_df.display()