import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Starting customer transformation with {len(df)} rows")

    clean_df = df.copy()

    # Standardize column names
    clean_df.columns = (
        clean_df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove exact duplicates
    clean_df = clean_df.drop_duplicates()

    # Normalize text fields
    clean_df["first_name"] = clean_df["first_name"].astype("string").str.strip().str.title()
    clean_df["last_name"] = clean_df["last_name"].astype("string").str.strip().str.title()
    clean_df["email"] = clean_df["email"].astype("string").str.strip().str.lower()

    # Convert dates
    clean_df["signup_date"] = pd.to_datetime(
        clean_df["signup_date"],
        errors="coerce",
        format="mixed"
    )

    # Convert numeric values
    clean_df["annual_spend"] = pd.to_numeric(
        clean_df["annual_spend"],
        errors="coerce"
    )

    # Remove rows missing critical fields
    clean_df = clean_df.dropna(
        subset=["first_name", "email"]
    )

    # Remove blank names/emails
    clean_df = clean_df[
        (clean_df["first_name"].str.strip() != "") &
        (clean_df["email"].str.strip() != "")
    ]

    clean_df = clean_df.reset_index(drop=True)

    logger.info(
        f"Customer transformation complete: {len(clean_df)} rows"
    )

    return clean_df
