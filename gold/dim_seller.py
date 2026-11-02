# Databricks notebook source
# DBTITLE 1,Load silver sellers
seller_df = spark.table("`olist-container-9pm`.silver.olist_sellers_dataset")

# COMMAND ----------

# DBTITLE 1,Create seller dimension
# Create Seller Dimension
seller_df = seller_df.withColumnRenamed("seller_id:", "seller_id").select(
    "seller_id",
    "seller_zip_code_prefix",
    "seller_city",
    "seller_state"
)

# COMMAND ----------

# DBTITLE 1,Write dim_seller to gold
seller_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("`olist-container-9pm`.gold.dim_seller")