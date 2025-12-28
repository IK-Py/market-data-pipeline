# Pipeline Architecture & System Design

## 1. System Overview
This project implements a serverless **ELT (Extract, Load, Transform)** architecture on AWS to manage financial market data. The goal is to provide a scalable, idempotent, and monitored pipeline for downstream data science and analytics.



## 2. Technical Workflow

### Phase 1: Extraction (AWS Lambda & Python)
* **Process:** A Python-based Lambda function authenticates with the Alpha Vantage API.
* **Data Strategy:** Fetch daily time-series JSON data.
* **Storage:** The raw JSON is persisted in an S3 "Landing Zone."
* **Design Choice:** Lambda was chosen for its zero-server overhead and cost-efficiency for short, bursty batch jobs.

### Phase 2: Data Lake Partitioning (Amazon S3)
* **Hierarchy:** `s3://[bucket-name]/raw/stock_data/YYYY-MM-DD/`
* **Standard:** Data is partitioned by date. This optimizes performance by allowing the Glue job to target specific timeframes, reducing unnecessary data scanning.

### Phase 3: Ingestion & Orchestration (AWS Glue)
* **Mechanism:** Glue Python Shell.
* **Performance:** Uses the Redshift `COPY` command. This is a best practice for high-volume ingestion, as it leverages Redshift’s Massively Parallel Processing (MPP) to load data from S3 in parallel.

### Phase 4: Transformation (Amazon Redshift SQL)
* **Staging:** Data is first loaded into `market_data.stg_stock_prices` to allow for raw validation.
* **Production:** A `DELETE-INSERT` (Upsert) pattern moves cleaned data into `market_data.fct_stock_prices`.
* **Optimization:** * **DISTKEY (symbol):** Colocates data for specific stocks to speed up joins.
    * **SORTKEY (price_date):** Optimizes time-series queries.



## 3. Configuration & Environment Variables
To ensure security and portability, the pipeline uses environment variables. These must be defined in a `.env` file in the project root.

| Key | Description | Example Format |
| :--- | :--- | :--- |
| `MARKET_API_KEY` | Alpha Vantage API Key | `X1Y2Z3A4B5` |
| `S3_BUCKET_NAME` | S3 Landing Zone Bucket Name | `my-market-data-lake` |
| `REDSHIFT_HOST` | Redshift Cluster Endpoint | `cluster.abc.us-east-1.redshift.amazonaws.com` |
| `REDSHIFT_PORT` | Redshift Port (Default 5439) | `5439` |
| `REDSHIFT_DB` | Redshift Database Name | `dev` |
| `REDSHIFT_USER` | Redshift Username | `awsuser` |
| `REDSHIFT_PASSWORD` | Redshift Password | `Password1245` |
| `REDSHIFT_IAM_ROLE_ARN` | IAM Role for Redshift S3 Access | `arn:aws:iam::123456789:role/RedshiftS3Role` |
| `AWS_REGION` | AWS Region for Resources | `us-east-1` |

## 4. Data Quality & Monitoring
Data integrity is maintained through an automated Python suite (`quality_checks.py`) that runs post-transformation:
1.  **Completeness:** Checks for NULLs in critical price columns.
2.  **Validity:** Ensures volume and price amounts are positive numbers.
3.  **Freshness:** Verifies that today's data has arrived in the warehouse.

## 5. Incident Resolution
All components utilize the Python `logging` module. In the event of a failure:
* **Lambda Errors:** Captured in CloudWatch logs.
* **Database Errors:** Transformation SQL is wrapped in transactions; any failure triggers a `ROLLBACK` to maintain database consistency