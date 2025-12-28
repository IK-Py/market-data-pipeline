/*
  PROJECT: Market Data Warehouse
  FILE: ddl_schema.sql
  DESCRIPTION: Defines the physical schema for the market data pipeline.
               Includes a Staging layer (Raw) and a Production layer (Fact).
  DEPENDENCIES: None
*/

-- Create a schema to keep things organized
CREATE SCHEMA IF NOT EXISTS market_data;

-- STAGING TABLE ("The "Raw" landing zone)
-- Use VARCHAR for most fields here to avoid ingestion errors
DROP TABLE IF EXISTS market_data.stg_stock_prices;
CREATE TABLE market_data.stg_stock_prices (
    symbol          VARCHAR(10),
    refresh_data    VARCHAR(20),
    open_price      VARCHAR(20),
    high_price      VARCHAR(20),
    low_price       VARCHAR(20),
    close_price     VARCHAR(20),
    volume          VARCHAR(20),
    extraction_date TIMESTAMP DEFAULT SYSDATE
);

-- PRODUCTION TABLE (The "Clean" table)
-- Use proper data types for optimization
DROP TABLE IF EXISTS market_data.fct_stock_prices;
CREATE TABLE market_data.fct_stock_prices (
    stock_id        INT IDENTITY(1,1),
    symbol          VARCHAR(10) NOT NULL,
    price_date      DATE NOT NULL,
    open_amt        DECIMAL(18, 4),
    high_amt        DECIMAL(18, 4),
    low_amt         DECIMAL(18, 4),
    close_amt       DECIMAL(18, 4),
    volume_cnt      BIGINT
    created_at      TIMESTAMP DEFAULT SYSDATE
)
DISTSTYLE KEY
DISTKEYY (symbol)
SORTKEY (price_data)

