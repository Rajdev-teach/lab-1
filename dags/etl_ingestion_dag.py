import logging
from datetime import datetime, timedelta

from airflow.decorators import dag, task

from dag_utils import (
    run_customer_pipeline,
    run_product_pipeline,
    run_order_pipeline,
)

logger = logging.getLogger(__name__)

default_args = {
    "owner": "data_eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="etl_ingestion_pipeline",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ingestion"],
)
def etl_ingestion_dag():

    @task
    def initialize_db():
        from pipeline.loaders.db_connection import init_db

        init_db()
        return True

    @task
    def etl_customers(db_initialized):
        return run_customer_pipeline()

    @task
    def etl_products(db_initialized):
        return run_product_pipeline()

    @task
    def etl_orders(db_initialized):
        return run_order_pipeline()

    @task
    def pipeline_summary(customers, products, orders):
        logger.info(
            "Pipeline Summary | customers=%s products=%s orders=%s",
            customers,
            products,
            orders,
        )

        return {
            "customers": customers,
            "products": products,
            "orders": orders,
        }

    init_done = initialize_db()

    customers_result = etl_customers(init_done)
    products_result = etl_products(init_done)
    orders_result = etl_orders(init_done)

    pipeline_summary(
        customers_result,
        products_result,
        orders_result,
    )


dag = etl_ingestion_dag()
