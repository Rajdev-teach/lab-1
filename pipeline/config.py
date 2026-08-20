import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
AIRFLOW_DATABASE_URL = os.getenv("AIRFLOW_DATABASE_URL")
API_URL = os.getenv("API_URL")
