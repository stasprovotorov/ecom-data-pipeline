.PHONY: up init-db etl dbt-run dbt-test pipeline

up:
	docker compose up -d

init-db:
	docker exec -i ecom_postgres psql -U postgres -d ecom < sql/init_schema.sql

etl:
	python3 -m venv .venv_etl && \
	. .venv_etl/bin/activate && \
	pip install -r requirements-etl.txt && \
	python3 -m src.etl_users && \
	python3 -m src.etl_products && \
	python3 -m src.etl_orders && \
	python3 -m src.etl_order_items

dbt-run:
	python3 -m venv .venv_dbt && \
	. .venv_dbt/bin/activate && \
	pip install -r requirements-dbt.txt && \
	cd ecom_dbt && \
	dbt run

dbt-test:
	. .venv_dbt/bin/activate && \
	cd ecom_dbt && \
	dbt test

pipeline:
	$(MAKE) up
	sleep 5
	$(MAKE) init-db
	$(MAKE) etl
	$(MAKE) dbt-run
	$(MAKE) dbt-test
