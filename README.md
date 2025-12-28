# End-to-End Market Data Warehouse (AWS ELT Pipeline)

A production-grade Data Engineering pipeline designed to automate the extraction, loading, and transformation (ELT) of financial market data. This project demonstrates a serverless architecture capable of handling batch data processing with built-in quality assurance.

## 🚀 Project Overview
This pipeline automates the journey of financial data from a third-party API (Alpha Vantage) into a structured Amazon Redshift Data Warehouse. It focuses on scalability, idempotency, and data integrity.



## 🛠 Tech Stack
* **Infrastructure:** AWS (Lambda, S3, Glue, Redshift, EventBridge)
* **Languages:** Python 3.9+, SQL (Redshift/PostgreSQL dialect)
* **Libraries:** `boto3`, `redshift-connector`, `requests`, `python-dotenv`
* **Orchestration:** EventBridge (Scheduling) & AWS Glue (ETL Jobs)

## 📁 Repository Structure
```text
.
├── src/                    # Python logic
│   ├── extract_lambda.py   # API extraction and S3 partitioning
│   ├── glue_transform.py   # Data movement and SQL orchestration
│   └── quality_checks.py   # Post-load data validation
├── sql/                    # Database logic
│   ├── ddl_schema.sql      # Staging and Fact table definitions
│   └── transformations.sql # Data cleaning and Upsert logic
├── docs/                   # Detailed documentation
│   ├── architecture.md     # System design & config keys
│   └── data_dictionary.md  # Schema and field definitions
├── .gitignore              # Git safety
├── requirements.txt        # Python dependencies
└── README.md               # Project overview
⚙️ Key Engineering Features
S3 Data Lake Partitioning: Implements a logical folder structure (raw/stock_data/YYYY-MM-DD/) to optimize data retrieval and storage costs.

Redshift COPY Performance: Utilizes the high-performance COPY command to ingest data from S3 in parallel, demonstrating knowledge of MPP (Massively Parallel Processing) databases.

Idempotent Design: Employs a DELETE-INSERT (Upsert) strategy in SQL to ensure the pipeline can be re-run for any date without creating duplicate records.

Automated Data Quality (DQC): Includes a validation suite to detect NULL values, invalid trade volumes, and data freshness issues before the data is delivered to analysts.

🔧 Installation & Setup
Clone the Repo:

Bash

git clone [https://github.com/yourusername/market-data-pipeline.git](https://github.com/yourusername/market-data-pipeline.git)
cd market-data-pipeline
Install Dependencies:

Bash

pip install -r requirements.txt
Configure Environment: Create a .env file based on the requirements listed in docs/architecture.md.

📈 Data Lineage
Extract: Lambda pulls JSON data from Alpha Vantage.

Load: Glue executes a COPY command into Redshift Staging.

Transform: SQL casts types and performs a clean "Upsert" into the Final Fact table.

Audit: Python verifies the final table for integrity.
