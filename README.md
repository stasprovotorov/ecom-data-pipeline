# E-commerce Data Pipeline

A local data engineering project that loads e-commerce CSV data into PostgreSQL, processes it with Python ETL, and builds analytical models with dbt.

## Stack

- Python
- PostgreSQL
- Docker Compose
- pandas
- SQLAlchemy
- dbt
- Makefile

## Pipeline

```text
CSV files -> Python ETL -> PostgreSQL raw tables -> dbt staging -> dbt marts
```

## Project Structure

```text
.
├── Makefile
├── data
│   ├── order_items.csv
│   ├── orders.csv
│   ├── products.csv
│   └── users.csv
├── docker-compose.yml
├── ecom_dbt
│   ├── dbt_project.yml
│   └── models
│       ├── marts
│       │   ├── dim_users.sql
│       │   ├── mart_daily_sales.sql
│       │   ├── mart_product_sales.sql
│       │   ├── mart_user_metrics.sql
│       │   └── schema.yml
│       └── staging
│           ├── schema.yml
│           ├── sources.yml
│           ├── stg_order_items.sql
│           ├── stg_orders.sql
│           ├── stg_products.sql
│           └── stg_users.sql
├── requirements-dbt.txt
├── requirements-etl.txt
├── sql
│   └── init_schema.sql
└── src
    ├── __init__.py
    ├── config.py
    ├── database.py
    ├── etl_order_items.py
    ├── etl_orders.py
    ├── etl_products.py
    ├── etl_users.py
    ├── logging_config.py
    ├── sql.py
    └── utils.py
```

## Data Models

**Raw tables**
- `raw_users`
- `raw_products`
- `raw_orders`
- `raw_order_items`

**dbt staging models**
- `stg_users`
- `stg_products`
- `stg_orders`
- `stg_order_items`

**Analytics models**
- `dim_users`
- `mart_daily_sales`
- `mart_product_sales`
- `mart_user_metrics`

## Setup

### 1. Create virtual environments

**ETL**
```bash
python3 -m venv .venv_etl
source .venv_etl/bin/activate
pip install -r requirements-etl.txt
deactivate
```

**dbt**
```bash
python3 -m venv .venv_dbt
source .venv_dbt/bin/activate
pip install -r requirements-dbt.txt
deactivate
```

### 2. Run the full pipeline
```bash
make pipeline
```

## Notes

The project uses two separate virtual environments:

- `.venv_etl` for Python ETL
- `.venv_dbt` for dbt

This helps keep dependencies isolated and avoids package conflicts.

## Future Improvements

- ETL logging
- orchestration
- incremental dbt models
- CI/CD
- dbt docs
- data quality checks
- investigate compatibility of ETL and dbt dependencies to use a single environment
