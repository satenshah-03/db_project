# Databricks notebook source
order_items_df = spark.table("`olist-container-9pm`.silver.olist_order_items_dataset")
order_df = spark.table("`olist-container-9pm`.silver.olist_orders_dataset")
customer_df = spark.table("`olist-container-9pm`.silver.olist_customers_dataset")


# COMMAND ----------

# DBTITLE 1,Join order items with orders and customers
fact_order_item = order_items_df \
    .join(
        order_df.select(
            "order_id",
            "customer_id",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ),
        "order_id",
        "left"
    ) \
    .join(
        customer_df.select(
            "customer_id",
            "customer_zip_code_prefix"
        ),
        "customer_id",
        "left"
    )


# COMMAND ----------

# DBTITLE 1,Select and rename fact columns
from pyspark.sql import functions as f

fact_order_items = fact_order_item.select(
    "order_id",
    "order_item_id",
    "customer_id",
    "product_id",
    "seller_id",
    "customer_zip_code_prefix",
    f.col("order_purchase_timestamp").alias("purchase_date"),
    f.col("order_approved_at").alias("approved_date"),
    f.col("order_delivered_carrier_date").alias("carrier_date"),
    f.col("order_delivered_customer_date").alias("delivered_date"),
    f.col("order_estimated_delivery_date").alias("estimated_delivery_date"),
    "shipping_limit_date",
    "price",
    "freight_value"
)


# COMMAND ----------

fact_order_items.display()

# COMMAND ----------

# DBTITLE 1,Write to gold.fact_order_items
fact_order_items.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("`olist-container-9pm`.gold.fact_order_items")