import logging
import sys
import time

from pipeline.utils.logger import setup_logging

from pipeline.extractors.csv_extractor import extract_csv
from pipeline.extractors.json_extractor import extract_json
from pipeline.extractors.api_extractor import extract_api

from pipeline.transformers.customer_transformer import transform_customers
from pipeline.transformers.product_transformer import transform_products
from pipeline.transformers.order_transformer import transform_orders

from pipeline.loaders.db_connection import SessionLocal, init_db
from pipeline.loaders.db_loader import (
    load_customers,
    load_products,
    load_orders,
)

from pipeline.config import API_URL

logger = logging.getLogger(__name__)


def run_customer_pipeline(session):
    raw = extract_csv("data/raw/customers.csv")
    clean = transform_customers(raw)
    loaded = load_customers(session, clean)

    return {
        "raw": len(raw),
        "clean": len(clean),
        "loaded": loaded,
    }


def run_product_pipeline(session):
    raw = extract_json("data/raw/products.json")
    clean = transform_products(raw)
    loaded = load_products(session, clean)

    return {
        "raw": len(raw),
        "clean": len(clean),
        "loaded": loaded,
    }


def run_order_pipeline(session):
    raw = extract_api(API_URL)
    clean = transform_orders(raw)
    loaded = load_orders(session, clean)

    return {
        "raw": len(raw),
        "clean": len(clean),
        "loaded": loaded,
    }


def run_pipeline() -> int:
    setup_logging()

    start_time = time.time()

    logger.info("Starting ETL pipeline")

    init_db()

    results = {}
    errors = {}

    pipelines = [
        ("customers", run_customer_pipeline),
        ("products", run_product_pipeline),
        ("orders", run_order_pipeline),
    ]

    with SessionLocal() as session:
        for name, runner in pipelines:
            try:
                logger.info(f"Starting {name} pipeline")

                results[name] = runner(session)

                logger.info(
                    f"{name} pipeline completed: {results[name]}"
                )

            except Exception as e:
                logger.exception(f"{name} pipeline failed")
                errors[name] = str(e)

    elapsed = round(time.time() - start_time, 2)

    logger.info(
        f"Pipeline summary | results={results} "
        f"errors={errors} elapsed={elapsed}s"
    )

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(run_pipeline())
