# Olist Pipeline Analysis

Analysis of the Lakeflow Job **"landing to bronze to silver pipeline"** that orchestrates this project
(as of 2026-11-02). A ready-to-import version of the job is in [`pipeline/olist_pipeline_job.json`](../pipeline/olist_pipeline_job.json).

## 1. Architecture

```
ADLS Gen2 (olist-container-9pm/landing/*.csv)
        |  external location + UC external volume  landing.files
        v
BRONZE  (9 tasks, parallel)   raw CSV -> Delta, explicit schema, + timestamp/source audit cols
        v
SILVER  (9 tasks)             lowercase/standardize, drop null keys, dropDuplicates on key
        v
GOLD    (9 tasks)             star schema: 6 dims + 3 facts
        v
ANALYTICS                     ad-hoc queries on gold (not part of the job)
```

* Catalog `olist-container-9pm`; schemas `landing`, `bronze`, `silver`, `gold` (each with its own ADLS managed location).
* All writes are Delta, `mode("overwrite")` (full refresh every run).
* Compute: serverless, performance-optimized. 27 notebook tasks, `max_concurrent_runs = 1`, queueing on.

## 2. Task DAG

| Dataset | Bronze task | Silver task | Gold task(s) |
| --- | --- | --- | --- |
| customers | customer_bronze_ingestion | customer_silver_transformation | dim_customer |
| geolocation | geolocation_bronze_ingestion | geolocation_silver_transformation | dim_location |
| orders | order_bronze_ingestion | order_silver_transformation | dim_order, dim_date |
| order items | orders_items_bronze_ingestion | orders_items_silver_transformation | fact_order_items (+ orders, customers) |
| payments | payment_bronze_ingestion | payment_silver_transformation | fact_payment (+ orders, customers) |
| reviews | review_bronze_ingestion | review_silver_transformation | fact_review (+ orders, customers) |
| products | product_bronze_ingestion | product_silver_transformation | dim_product (+ category translation) |
| category translation | category_name_translation_bronze | category_name_translation_silver | (feeds dim_product) |
| sellers | seller_bronze_ingestion | seller_silver_transformation | dim_seller |

Gold outputs: `dim_customer`, `dim_location`, `dim_order`, `dim_date`, `dim_products`, `dim_seller`,
`fact_order_items`, `fact_payments`, `fact_reviews`.

## 3. Run history and performance

| Metric | Value |
| --- | --- |
| Runs analysed | 8 (2026-10-30 to 2026-11-02) |
| Result | 5 succeeded, 2 failed, 1 cancelled |
| Failure causes | Task pointing to a non-existent notebook (`items_bronze data ingestion`), and one customer bronze code error. Both fixed. |
| Latest run (886631307952855) | 180 s end to end, all 27 tasks succeeded on first attempt |
| Bronze tasks | ~80-99 s each (run in parallel) |
| Silver tasks | ~46-59 s each |
| Gold tasks | ~18-40 s each |
| Critical path | order_items bronze (99 s) -> silver (48 s) -> fact_order_items (37 s) |

The data is small (largest CSV ~61 MB), so most task time is per-task startup and session overhead rather than Spark work.
Databricks run insights found no compute issues; they flagged only minor redundant grouping aggregates
(on `customer_id`, `order_purchase_timestamp`, `seller_id:`), e.g. `dropDuplicates` on keys that are already unique.

## 4. Findings

### Correctness
1. **Missing dependency:** in the workspace job, `fact_payment` reads `silver.olist_payment_dataset` but depends only on
   the order and customer silver tasks, not `payment_silver_transformation`. It can read stale payments.
   *Fixed in `pipeline/olist_pipeline_job.json`.*
2. **Column name quirk:** `silver.olist_sellers_dataset` has a column literally named `seller_id:`; it is renamed only in `dim_seller`.
   Better to clean it in the bronze or silver layer.
3. **Duplicate product logic:** `gold/build product dimension` and `gold/dim_product` both build the product dimension;
   only `dim_product` (writes `gold.dim_products`) is used by the job.
4. **Naming inconsistency:** gold tables mix singular and plural (`dim_order` vs `dim_products`, `fact_payments`), and silver uses
   `olist_payment_dataset` (singular) while the source file is `olist_order_payments_dataset.csv`.

### Reliability and operations
5. No schedule or trigger. The job only runs manually.
6. No retries and no job-level timeout (`timeout_seconds = 0`).
7. Notifications are configured only on the `seller_bronze_ingestion` task (on start/success/failure), not at the job level.
8. No data-quality checks (row counts, null/unique key checks) between layers.

### Maintainability and cost
9. The catalog name and storage paths are hard-coded in every notebook. Use job parameters or widgets (`catalog`, `landing_path`).
10. Notebooks contain ~85 `display()` calls that run during job execution and trigger extra Spark actions.
11. 27 separate notebooks with near-identical bronze/silver code. Could be a single parameterised notebook (one task per
    dataset via a For each task) or a Lakeflow Spark Declarative Pipeline.
12. Full overwrite every run. Fine for this static dataset; switch to incremental (Auto Loader / MERGE) if new files arrive regularly.
13. Job notebooks run from the workspace home folder, while this repo holds copies, so the two can drift apart.
    Running the job from Git (`source: GIT`) removes the drift.

## 5. Recommended job settings (applied in `pipeline/olist_pipeline_job.json`)

* Notebooks run from this GitHub repo (`git_source`, branch `main`).
* `fact_payment` now depends on `payment_silver_transformation`.
* `max_retries: 1` per task, job timeout 1 hour, failure email at job level.

## 6. How to create the job from this repo

1. Replace `<YOUR_EMAIL>` in `pipeline/olist_pipeline_job.json` (and the git URL if you fork the repo).
2. Complete the setup in the README (storage credential, external location, catalog/schemas/volume, CSV upload).
3. Create the job with the Databricks CLI:
   `databricks jobs create --json @pipeline/olist_pipeline_job.json`
   or use the UI: **Jobs & Pipelines > Create > Job**, then switch the editor to JSON/YAML and paste the definition.
4. Optionally add a schedule (e.g. daily) in the job's **Schedules & Triggers** panel.
