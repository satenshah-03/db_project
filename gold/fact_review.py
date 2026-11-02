# Databricks notebook source
# DBTITLE 1,Load silver tables
reviews_df = spark.table("`olist-container-9pm`.silver.olist_reviews_dataset")
orders_df = spark.table("`olist-container-9pm`.silver.olist_orders_dataset")
customers_df = spark.table("`olist-container-9pm`.silver.olist_customers_dataset")
customers_df.show(5)


# COMMAND ----------

reviews_df = reviews_df.join( orders_df , on='order_id' , how='left' )
reviews_df = reviews_df.join(customers_df,on=['customer_id'], how='left')
reviews_df.show(5)


# COMMAND ----------

reviews_df = reviews_df.select(
    "order_id",
    "review_id",
    "customer_id",
    "customer_zip_code_prefix",
    "review_creation_date",
    "review_answer_timestamp",
    "review_score",
    "review_comment_title",
    "review_comment_message"
)


# COMMAND ----------

reviews_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("`olist-container-9pm`.gold.fact_reviews")


# COMMAND ----------

# MAGIC %sql
# MAGIC select * from `olist-container-9pm`.gold.fact_reviews
# MAGIC