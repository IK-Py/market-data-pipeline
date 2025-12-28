"""
Data Quality Audit Script: Redshift Validation

This module performs automated data quality checks (DQC) on the production 
tables. It ensures that the transformation logic preserved data integrity 
and that no 'garbage data' entered the analytical layer.
"""

import os
import logging
import redshift_connector

from dotenv import load_dotenv

# Setup logging for pipeline health monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


def run_quality_checks():
    """
    Executes a suite of SQL-based audits against the Redshift warehouse.
    """
    conn = redshift_connector.connect(
        host=os.getenv('REDSHIFT_HOST'),
        database=os.getenv('REDSHIFT_DB'),
        user=os.getenv('REDSHIFT_USER'),
        password=os.getenv('REDSHIFT_PASSWORD')
    )
    cursor = conn.cursor()

    # Define 'Tests' as a dictionary of SQL queries and expected results
    # Each query should return 0 if the data is HEALTHY
    checks = {
        "NULL_CHECK": {
            "query": "SELECT COUNT(*) FROM market_data.fct_stock_prices WHERE close_amt IS NULL;",
            "expected": 0,
            "error_msg": "Null values found in critical 'close_amt' column!"
        },
        "ZERO_VOLUME_CHECK": {
            "query": "SELECT COUNT(*) FROM market_data.fct_stock_prices WHERE volume_cnt <= 0;",
            "expected": 0,
            "error_msg": "Invalid trade volume detected (zero or negative)!"
        },
        "FUTURE_DATE_CHECK": {
            "query": "SELECT COUNT(*) FROM market_data.fct_stock_prices WHERE price_date > CURRENT_DATE;",
            "expected": 0,
            "error_msg": "Future dates detected in price data!"
        },
        "FRESHNESS_CHECK": {
            "query": "SELECT COUNT(*) FROM market_data.fct_stock_prices WHERE price_date = CURRENT_DATE;",
            "expected": 1,  # Expect at least today's data for the symbol
            "error_msg": "Fresh data for today is missing!"
        }
    }

    passed_all = True

    try:
        for check_name, check_meta in checks.items():
            cursor.execute(check_meta["query"])
            result = cursor.fetchone()[0]

            if check_name == "FRESHNESS_CHECK":
                if result < check_meta["expected"]:
                    logger.error(
                        f"FAIL: {check_name} - {check_meta['error_msg']}")
                    passed_all = False
            elif result > check_meta["expected"]:
                logger.error(
                    f"FAIL: {check_name} - {check_meta['error_msg']} (count: {result})")
                passed_all = False
            else:
                logger.info(f"PASS: {check_name}")

        if passed_all:
            logger.info("All Data Quality checks completed successfully.")
        else:
            logger.warning(
                "Data Quality checks completed with failues. Incident resolution required.")

    except Exception as e:
        logger.error(f"Quality Check execution failed: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    run_quality_checks()