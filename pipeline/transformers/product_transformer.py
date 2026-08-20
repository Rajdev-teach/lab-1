import logging
import pandas as pd

logger = logging.getLogger(__name__)

ALLOWED_CATEGORIES = {
    "Electronics",
    "Kitchen",
    "Furniture"
}


def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Starting product transformation with {len(df)} rows")

    clean_df = df.copy()

    # Standardize column names
    clean_df.columns = (
        clean_df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove duplicate product IDs
    clean_df = clean_df.drop_duplicates(
        subset=["product_id"],
        keep="first"
    )

    # Clean text fields
    clean_df["name"] = (
        clean_df["name"]
        .astype("string")
        .str.strip()
    )

    clean_df["category"] = (
        clean_df["category"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    # Convert numeric columns
    clean_df["price"] = pd.to_numeric(
        clean_df["price"],
        errors="coerce"
    )

    clean_df["stock"] = pd.to_numeric(
        clean_df["stock"],
        errors="coerce"
    ).fillna(0)

    clean_df["rating"] = pd.to_numeric(
        clean_df["rating"],
        errors="coerce"
    )

    # Convert datetime
    clean_df["created_at"] = pd.to_datetime(
        clean_df["created_at"],
        errors="coerce"
    )

    # Apply business rules
    clean_df = clean_df[
        clean_df["category"].isin(ALLOWED_CATEGORIES)
    ]

    clean_df = clean_df[
        clean_df["price"] > 0
    ]

    clean_df = clean_df[
        clean_df["rating"].between(0, 5)
    ]

    clean_df = clean_df.reset_index(drop=True)

    logger.info(
        f"Product transformation complete: {len(clean_df)} rows"
    )

    return clean_df
