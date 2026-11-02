# Databricks notebook source
pdf=spark.read.table('`olist-container-9pm`.gold.dim_products')
pdf.show(5)

# COMMAND ----------

odf=spark.read.table('`olist-container-9pm`.gold.dim_order')
odf.show(5)

# COMMAND ----------

fdf=spark.read.table('`olist-container-9pm`.gold.fact_payments')
fdf.show(5)

# COMMAND ----------

odf=odf.join(fdf,on='order_id',how='left').select('order_id','payment_value')
odf.show()

# COMMAND ----------

odif=spark.read.table('`olist-container-9pm`.silver.olist_order_items_dataset')
odif.show(5)