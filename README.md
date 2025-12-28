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
