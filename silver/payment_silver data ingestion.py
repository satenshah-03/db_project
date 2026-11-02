# Databricks notebook source
payments_df=spark.read.table('`olist-container-9pm`.bronze.olist_payment_dataset')
payments_df.display()

# COMMAND ----------

payments_df=payments_df.dropDuplicates(['order_id'])
payments_df=payments_df.filter(payments_df['payment_value']>0)
payments_df.display()


# COMMAND ----------

payments_df.write.format('delta').mode('overwrite').saveAsTable('`olist-container-9pm`.silver.olist_payment_dataset')
payments_df.display()