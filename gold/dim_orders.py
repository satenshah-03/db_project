# Databricks notebook source
order_df = spark.table("`olist-container-9pm`.silver.olist_orders_dataset")


# COMMAND ----------

order_df = order_df.select(
    "order_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
)

# COMMAND ----------

order_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("`olist-container-9pm`.gold.dim_order")
