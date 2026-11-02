# Databricks notebook source
product_df=spark.read.table('`olist-container-9pm`.silver.olist_products_dataset')
category_df=spark.read.table('`olist-container-9pm`.silver.product_category_name_translation')
display(product_df)
display(category_df)

# COMMAND ----------

# MAGIC %md
# MAGIC join product with English category name

# COMMAND ----------

# DBTITLE 1,Join product with English category
product_df=product_df.join(
    category_df, 
    on=('product_category_name'),
    how='left'
).select('product_id','product_category_name','product_category_name_english','product_name_lenght','product_description_lenght','product_photos_qty','product_weight_g','product_length_cm','product_height_cm','product_width_cm')
product_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC write to Gold

# COMMAND ----------

product_df.write\
    .format("delta")\
    .mode("overwrite")\
    .saveAsTable("`olist-container-9pm`.gold.dim_products")

# COMMAND ----------

# MAGIC %sql
# MAGIC select*from `olist-container-9pm`.gold.dim_products