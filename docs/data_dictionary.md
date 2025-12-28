# Data Dictionary: Market Data Warehouse

This document provides a detailed breakdown of the schema and business logic for the tables within the Amazon Redshift Warehouse.

---

## 1. Staging Layer
**Table Name:** `market_data.stg_stock_prices`  
**Description:** A temporary landing table used for raw ingestion from S3 via the `COPY` command. Data in this table is ephemeral and is truncated after each successful transformation run.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `symbol` | VARCHAR(10) | The stock ticker symbol (e.g., AAPL, TSLA). |
| `refresh_date` | VARCHAR(20) | Raw date string provided by the API. |
| `open_price` | VARCHAR(20) | Raw opening price string. |
| `high_price` | VARCHAR(20) | Raw daily high price string. |
| `low_price` | VARCHAR(20) | Raw daily low price string. |
| `close_price` | VARCHAR(20) | Raw closing price string. |
| `volume_cnt` | VARCHAR(20) | Raw trading volume string. |

---

## 2. Production Layer (Fact Table)
**Table Name:** `market_data.fct_stock_prices`  
**Description:** The primary analytical table containing cleaned, type-cast, and deduplicated historical price data.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `stock_id` | INT | IDENTITY(1,1) | Auto-incrementing unique identifier for each record. |
| `symbol` | VARCHAR(10) | **DISTKEY** | The stock ticker symbol. Used as the distribution key to optimize join performance. |
| `price_date` | DATE | **SORTKEY** | The date the market activity occurred. Used as the sort key for time-series filtering. |
| `open_amt` | DECIMAL(18, 4) | - | The price at which the stock first traded upon market opening. |
| `high_amt` | DECIMAL(18, 4) | - | The highest price reached during the trading day. |
| `low_amt` | DECIMAL(18, 4) | - | The lowest price reached during the trading day. |
| `close_amt` | DECIMAL(18, 4) | - | The final price at which the stock traded when the market closed. |
| `volume_cnt` | BIGINT | - | Total number of shares traded during the day. |
| `created_at` | TIMESTAMP | - | Audit column: Timestamp of when the record was inserted into the warehouse. |



---

## 3. Transformation Logic
* **Deduplication:** The `symbol` and `price_date` columns form a logical composite unique key. The pipeline uses a `DELETE-INSERT` pattern to ensure no duplicate records exist for the same symbol on the same date.
* **Precision:** All currency values are stored as `DECIMAL(18, 4)` to prevent the rounding errors associated with `FLOAT` or `REAL` types.
* **Storage:** The table uses **ZSTD** compression encoding to minimize storage footprint on Redshift.