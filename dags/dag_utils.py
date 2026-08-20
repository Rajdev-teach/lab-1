from pipeline.extractors.csv_extractor import extract_csv
from pipeline.extractors.json_extractor import extract_json
from pipeline.extractors.api_extractor import extract_api

from pipeline.transformers.customer_transformer import transform_customers
from pipeline.transformers.product_transformer import transform_products
from pipeline.transformers.order_transformer import transform_orders

from pipeline.loaders.db_connection import SessionLocal
from pipeline.loaders.db_loader import (
    load_customers,
    load_products,
    load_orders,
)

from pipeline.config import API_URL


def run_customer_pipeline():
    with SessionLocal() as session:
        raw = extract_csv("data/raw/customers.csv")
        clean = transform_customers(raw)
        loaded = load_customers(session, clean)

        return {
            "raw": len(raw),
            "clean": len(clean),
            "loaded": loaded,
        }


def run_product_pipeline():
    with SessionLocal() as session:
        raw = extract_json("data/raw/products.json")
        clean = transform_products(raw)
        loaded = load_products(session, clean)

        return {
            "raw": len(raw),
            "clean": len(clean),
            "loaded": loaded,
        }


def run_order_pipeline():
    with SessionLocal() as session:
        raw = extract_api(API_URL)
        clean = transform_orders(raw)
        loaded = load_orders(session, clean)

        return {
            "raw": len(raw),
            "clean": len(clean),
            "loaded": loaded,
        }
