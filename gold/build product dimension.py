# Databricks notebook source
product_df=spark.read.table('`olist-container-9pm`.silver.olist_products_dataset')
product_df.display()

# COMMAND ----------

translation_df=spark.read.table('`olist-container-9pm`.silver.product_category_name_translation')
translation_df.display()

# COMMAND ----------

product_df=product_df.join(translation_df,on=['product_category_name'],how='left')
product_df.display()

# COMMAND ----------

product_df=product_df.withColumn('volume',product_df['product_length_cm']*product_df['product_height_cm']*product_df['product_width_cm'])
product_df.display()

# COMMAND ----------

product_df=product_df.select(
                            ['product_id','product_category_name','product_category_name_english','product_description_lenght','product_name_lenght','product_length_cm','product_photos_qty','product_weight_g','product_width_cm','product_height_cm','volume']
)
product_df.display()

# COMMAND ----------

