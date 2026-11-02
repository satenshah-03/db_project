# Databricks notebook source
# DBTITLE 1,Load silver tables
payment_df = spark.table("`olist-container-9pm`.silver.olist_payment_dataset")
order_df = spark.table("`olist-container-9pm`.silver.olist_orders_dataset")
customer_df = spark.table("`olist-container-9pm`.silver.olist_customers_dataset")

# COMMAND ----------

fact_payment= payment_df \
    .join(
        order_df.select(
            "order_id",
            "customer_id",
            "order_purchase_timestamp"
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

fact_payments = fact_payment.select(
    "order_id",
    "payment_sequential",
    "customer_id",
    "customer_zip_code_prefix",
    "order_purchase_timestamp",
    "payment_type",
    "payment_installments",
    "payment_value"
)


# COMMAND ----------

fact_payments.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("`olist-container-9pm`.gold.fact_payments")