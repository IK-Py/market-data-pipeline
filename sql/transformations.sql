/*
  PROJECT: Market Data Warehouse
  FILE: transformations.sql
  DESCRIPTION: Orchestrates the ELT process from Staging to Production.
               Includes data type casting, deduplication (Upsert), 
               and staging cleanup.
  RELIANCE: Requires market_data.stg_stock_prices to be populated.
*/

-- CLEANING AND CASTING
-- Use a Common Table Expression (CTE) to format the data
WITH cleaned_data AS (
    SELECT
        symbol,
        TO_DATE(refresh_date, 'YYYY-MM-DD') as price_date,
        CAST(open_price AS DECIMAL(18, 4)) as open_amt,
        CAST(high_price AS DECIMAL(18, 4)) as high_amt,
        CAST(low_price AS DECIMAL(18, 4)) as low_amt,
        CAST(volume AS BIGINT) as volume_cnt
    FROM martket_data.stg_stock_prices
    WHERE refresh_date IS NOT NULL
)

-- THE UPSERT (Preventing Duplicates)
-- First, delete rows in Production that are about to re-insert
-- (This allows us to 're-run' the pipeline without doubling data)
DELETE FROM market_data.fct_stock_prices
USING cleaned_data
WHERE market_data.fct_stock_prices.symbol = cleaned_data.symbol
  AND market_data.fct_stock_prices.price_date = cleaned_data.price_date;

-- INSERT CLEAN DATA
INSERT INFO market_data.fct_stock_prices (
    symbol,
    price_date,
    open_amt,
    high_amt,
    low_amt,
    close_amt,
    volume_cnt
)
SELECT * FROM cleaned_data;

-- TRUNCATE STAGING
-- Clear the staging table so it's ready for tomorrow's batch
TRUNCATE TABLE market_data.stg_stock_prices;
