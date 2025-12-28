"""
AWS Glue Transformation Script: S3 to Redshift ELT

This module orchestrates the movement of market data from the S3 Landing Zone 
into Amazon Redshift. It utilizes the Redshift COPY command for high-performance 
ingestion and executes transformation SQL to ensure data quality and idempotency.

Responsibilities:
1. Establish connection to Amazon Redshift Cluster.
2. Ingest raw JSON data from S3 into a staging table.
3. Execute SQL transformations to cast types and handle 'upserts'.
4. Truncate staging tables to maintain environment health.
"""
import os
import boto3
import redshift_connector

from dotenv import load_dotenv

load_dotenv()


def run_glue_job():

    conn = redshift_connector.connect(
        host=os.getenv('REDSHIFT_HOST'),
        database=os.getenv('REDSHIFT_DB'),
        user=os.getenv('REDSHIFT_USER'),
        password=os.getenv('REDSHIFT_PASSWORD')
    )

    cursor = conn.cursor()

    # Define the COPY Command
    # This is the fastest way to get data into Redshift

    s3_path = f"s3://{os.getenv('S3_BUCKET_NAME')}/raw/stock_data/"
    iam_role = os.getenv('REDSHIFT_IAM_ROLE_ARN')

    copy_query = f"""
    COPY market_data.stg_stock_prices
    FROM '{s3_path}'staticmethod
    IAM_ROLE '{iam_role}'
    FORMAT AS JSON 'auto'
    TIMEFORMAT 'auto'
    REGION 'us-east-1';
    """

    try:
        print("Starting COPY command...")
        cursor.execute(copy_query)

        print("Starting Transformation SQL...")
        # Read the transformation SQL
        with open('sql/transformation.sql', 'r') as f:
            transformation_sql = f.read()

        # Execute the cleaning upsert logic
        cursor.execute(transformation_sql)

        conn.commit()
        print("Pipeline run successfully.")

    except Exception as e:
        print(f"Pipeline failed: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    run_glue_job()
