import logging

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


def extract_api(url: str, params: dict = None) -> pd.DataFrame:
    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        logger.info(f"Fetching data from {url}")

        response = session.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, (list, dict)):
            df = pd.json_normalize(data)
        else:
            raise TypeError(
                f"Unsupported API response type: {type(data).__name__}"
            )

        logger.info(
            f"Extracted {df.shape[0]} rows and "
            f"{df.shape[1]} columns from API"
        )

        return df

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise
