.PHONY: up init-db etl dbt-run dbt-test pipeline

up:
	docker compose up -d

init-db:
	docker exec -i ecom_postgres psql -U postgres -d ecom < sql/init_schema.sql

etl:
	. .venv_etl/bin/activate && \
	python -m src.etl_users && \
	python -m src.etl_products && \
	python -m src.etl_orders && \
	python -m src.etl_order_items

dbt-run:
	. .venv_dbt/bin/activate && \
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
