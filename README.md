# Automated Data Ingestion Pipeline

## Overview

This project implements a production-style ETL pipeline that extracts data from CSV, JSON, and REST API sources, transforms the data using Pandas, loads it into PostgreSQL, and orchestrates the workflow using Apache Airflow.

## Technologies

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Apache Airflow
- REST API
- Git & GitHub

## Pipeline Architecture

CSV / JSON / REST API → Extract → Transform → PostgreSQL → Apache Airflow

## Data Sources

- Customers: CSV
- Products: JSON
- Orders: JSONPlaceholder REST API

## Project Structure

```text
lab-1/
├── dags/
│   ├── dag_utils.py
│   └── etl_ingestion_dag.py
├── data/raw/
│   ├── customers.csv
│   └── products.json
├── pipeline/
│   ├── extractors/
│   ├── transformers/
│   ├── loaders/
│   └── utils/
├── main.py
├── requirements.txt
└── README.md
```

## ETL Process

1. Extract data from CSV, JSON, and REST API sources.
2. Clean and transform the data using Pandas.
3. Remove duplicates and handle missing values.
4. Standardize text, dates, and numeric values.
5. Load clean data into PostgreSQL.
6. Use UPSERT logic to prevent duplicate records.
7. Orchestrate the pipeline using Apache Airflow.

## Airflow DAG

DAG: `etl_ingestion_pipeline`

```text
initialize_db
      |
      +---- etl_customers ----+
      +---- etl_products -----+--> pipeline_summary
      +---- etl_orders -------+
```

## Results

| Dataset | Raw | Clean | Loaded |
|---|---:|---:|---:|
| Customers | 8 | 6 | 6 |
| Products | 8 | 6 | 6 |
| Orders | 100 | 100 | 100 |

Final PostgreSQL row counts:

- Customers: 6
- Products: 6
- Orders: 100

The pipeline was executed multiple times and the row counts remained unchanged, confirming idempotent UPSERT behavior.

## Running the Pipeline

Use Python 3.10 or newer and an existing PostgreSQL database. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, activate with `.\.venv\Scripts\Activate.ps1` and copy the configuration with `Copy-Item .env.example .env`.

Edit `.env` to set `DATABASE_URL` for your PostgreSQL database and user. The `API_URL` example reads synthetic orders from JSONPlaceholder. The pipeline creates its tables; the database must already exist. Keep the real `.env` file out of version control.

```bash
python main.py
```

The requirements above cover the standalone ETL pipeline. Install Apache Airflow separately, with its matching Python constraints, only when running the DAGs in `dags/`.

## Author

Rajdev Kumar Pulivarthi