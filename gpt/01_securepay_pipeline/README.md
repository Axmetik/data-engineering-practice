# SecurePay Pipeline

A learning data engineering project for processing financial transactions.

## Goal

Build a clean ETL pipeline that reads transaction batches, validates records, separates invalid/unmapped records into quarantine, enriches valid transactions with customer data, and produces processed outputs.

## Input files

- `data/sample/customers.csv`
- `data/sample/transactions_batch_001.csv`

## Pipeline stages

1. Extract CSV files
2. Validate schema and data quality
3. Quarantine invalid records
4. Transform and enrich valid records
5. Save processed outputs
6. Add tests

## Data quality rules

A transaction is valid only if:

- `tx_id` is not null
- `cust_id` is not null
- `tx_timestamp` can be parsed as datetime
- `amount` is numeric
- `amount` is greater than 0
- `cust_id` exists in `customers.csv`
- duplicate `tx_id` values are handled explicitly

## How to run

To be added.