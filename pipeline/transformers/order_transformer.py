import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Starting order transformation with {len(df)} rows")

    clean_df = df.copy()

    # Rename API fields
    clean_df = clean_df.rename(
        columns={
            "id": "order_id",
            "userId": "customer_id",
            "title": "order_title",
            "body": "order_description"
        }
    )

    # Keep only required columns
    clean_df = clean_df[
        [
            "order_id",
            "customer_id",
            "order_title",
            "order_description"
        ]
    ]

    # Drop rows with missing keys
    clean_df = clean_df.dropna(
        subset=["order_id", "customer_id"]
    )

    # Convert IDs to integers
    clean_df["order_id"] = pd.to_numeric(
        clean_df["order_id"],
        errors="coerce"
    )

    clean_df["customer_id"] = pd.to_numeric(
        clean_df["customer_id"],
        errors="coerce"
    )

    clean_df = clean_df.dropna(
        subset=["order_id", "customer_id"]
    )

    clean_df["order_id"] = clean_df["order_id"].astype(int)
    clean_df["customer_id"] = clean_df["customer_id"].astype(int)

    # Add synthetic timestamp
    clean_df["ingested_at"] = pd.Timestamp.now(tz="UTC")

    clean_df = clean_df.reset_index(drop=True)

    logger.info(
        f"Order transformation complete: {len(clean_df)} rows"
    )

    return clean_df
