"""
AWS Lambda Extraction Script: API to S3 Ingestion

This module handles the 'Extract' phase of the data pipeline. It fetches daily 
market data from the Alpha Vantage API and persists the raw JSON response into 
the Amazon S3 'Landing Zone'.

Key Features:
1. Environment-based configuration for API security.
2. Structured logging for pipeline health monitoring and troubleshooting.
3. Defensive error handling for API limits and network failures.
4. Data Lake partitioning logic (files are stored by date/symbol).
"""
import os
import json
import boto3
import requests
import logging

from datetime import datetime
from dotenv import load_dotenv

# Initialize logging for troubleshooting
logger = logging.getLogger()
logger.setLevel(logging.INFO)

load_dotenv()


def lambda_handler(event, context):
    """
    Extracts daily stock data from Alpha Vantage and saves to S3
    """
    # Setup Configuration
    api_key = os.getenv('MARKET_API_KEY')
    bucket_name = os.getenv('S3_BUCKET_NAME')
    symbol = "IBM"

    # Extract Data
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'

    try:
        logger.info(f"Fetching data for {symbol}...")
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        # Check if the API returned an error message
        if "Error Message" in data or "Information" in data:
            logging.error(
                f"API Error: {data.get('Error Message') or data.get('Information')}")
            return {"StatusCode": 400, "body": "API Limit reached or invalid symbol"}

        # Load to S3
        s3 = boto3.client('s3')

        # Organize by date to create a 'Data Lake' structure
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_path = f"raw/stock_data/{current_date}/{symbol}_daily.json"

        s3.put_object(
            Bucket=bucket_name,
            Key=file_path,
            Body=json.dumps(data)
        )

        logger.info(
            f"Successfully saved data to s3://{bucket_name}/{file_path}")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


# For local testing
if __name__ == "__main__":
    print(lambda_handler(None, None))
