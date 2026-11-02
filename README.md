# Olist E-commerce Medallion Project (Databricks)

End-to-end lakehouse project on the Brazilian Olist e-commerce dataset using a medallion architecture
(landing -> bronze -> silver -> gold) on Databricks with Unity Catalog and Azure Data Lake Storage (ADLS Gen2).

## Repository layout

| Folder | Contents |
| --- | --- |
| `setup/` | External location / storage access, catalog + schema + volume creation |
| `bronze/` | Raw CSV ingestion from the landing zone (one notebook per dataset) |
| `silver/` | Cleansing and standardization into `silver.*` tables |
| `gold/` | Star schema: dimensions (`dim_*`) and facts (`fact_*`) |
| `analytics/` | Analysis queries on the gold layer |

## Prerequisites

1. A Databricks workspace with Unity Catalog enabled.
2. An ADLS Gen2 container with the Olist CSV files under `landing/`:
   `olist_customers_dataset.csv`, `olist_geolocation_dataset.csv`, `olist_order_items_dataset.csv`,
   `olist_order_payments_dataset.csv`, `olist_order_reviews_dataset.csv`, `olist_orders_dataset.csv`,
   `olist_products_dataset.csv`, `olist_sellers_dataset.csv`, `product_category_name_translation.csv`
   (dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
3. A Unity Catalog storage credential with access to that container.

## Configuration to change before running

The code references the original author's environment. Replace these with your own values:

* Storage credential: `olist_storage_credential_9pm`
* External location: `olist_ext_loc_9pm`
* Storage URL: `abfss://olist-container-9pm@olistadls9pm2.dfs.core.windows.net/`
* Catalog: `olist-container-9pm` (needs backticks in SQL because of the hyphens), plus the schemas/volumes created in `setup/create catalog, schema, volume`

## Run order

1. `setup/access to cloud storage`
2. `setup/create catalog, schema, volume`
3. All notebooks in `bronze/` (independent of each other)
4. All notebooks in `silver/` (each depends on its matching bronze notebook)
5. `gold/` dimensions: `dim_customer`, `dim_location`, `dim_seller`, `dim_product` / `build product dimension`, `dim_orders`, `dim_date`
6. `gold/` facts: `fact_order_items`, `fact_payment`, `fact_review`
7. `analytics/Analytics`

Tip: a ready-to-import Lakeflow Job definition (27 tasks, runs notebooks straight from this repo) is in
`pipeline/olist_pipeline_job.json`. See `docs/PIPELINE_ANALYSIS.md` for the pipeline analysis and setup steps.

## Known data quirks

* In `silver.olist_sellers_dataset` the seller key column is literally named `seller_id:` (trailing colon); `dim_seller` renames it to `seller_id`.
* Payments silver table is `olist_payment_dataset` (singular).
* Some notebooks reassign the same DataFrame variable, so re-run the load cell before re-running transform cells.
