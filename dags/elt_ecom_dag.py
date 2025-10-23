import os
import io
import pandas as pd
from datetime import datetime, timedelta
import subprocess
from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from google.cloud import bigquery
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.bash import BashOperator

# ------------------------------
# Load environment variables
# ------------------------------
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

GCS_BUCKET = os.getenv("GCS_BUCKET")
BQ_DATASET = os.getenv("BQ_DATASET")

BQ_TABLE_ECOM_PRODUCTS = os.getenv("BQ_TABLE_ECOM_PRODUCTS")
BQ_TABLE_ECOM_CUSTOMERS = os.getenv("BQ_TABLE_ECOM_CUSTOMERS_ECOM")
BQ_TABLE_ECOM_ORDERS = os.getenv("BQ_TABLE_ECOM_ORDERS")

DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR")
DBT_PROFILES_DIR = os.getenv("DBT_PROFILES_DIR")

POSTGRES_CONN_URI = os.getenv("POSTGRES_CONN")

# GCS Object path (hardcoded example; can be dynamic later)
GCS_OBJECT = "ecom_raw/products.csv"

@dag(
    dag_id="elt_ecommerce",
    schedule="@daily",
    start_date=datetime.now() - timedelta(days=1),                                  # sets the first execution date of the DAG. here's saying "start from yesterday". Why yesterday? because Airflow's scheduler runs tasks for logical dates in the past. Example: if you start today, it'll consider "yesterday's data" as the first logical run. So the DAG behavior is deterministic (Airflow best practice).
    catchup=False,
    tags=["ecommerce", "elt"],
)
def elt_ecommerce():

    # ------------------------
    # 🧩 EXTRACT GROUP
    # ------------------------
    with TaskGroup("EXTRACTING_FROM_MULTIPLE_SOURCES", tooltip="Extract data from various sources") as extract_group:

        # --- Extract from MockAPI ---
        @task
        def extract_from_api():
            http_hook = HttpHook(http_conn_id="mockapi_default", method="GET")
            response = http_hook.run(endpoint="/ecom_orders_api/orders")
            data = response.json()
            df = pd.DataFrame(data)
            return df.to_json(orient="records")

        # --- Extract from Neon Postgres ---
        @task
        def extract_from_postgres():
            pg_hook = PostgresHook(postgres_conn_id="neon_postgres_default")
            sql = "SELECT * FROM customers"
            df = pg_hook.get_pandas_df(sql)
            return df.to_json(orient="records")

        # --- Wait for GCS File ---
        file_sensor = GCSObjectExistenceSensor(
            task_id="wait_for_gcs_file",
            bucket=GCS_BUCKET,
            object=GCS_OBJECT,
            poke_interval=30,
            timeout=600,
        )

        # --- Extract from GCS ---
        @task
        def extract_from_gcs():
            gcs_hook = GCSHook()
            file_bytes = gcs_hook.download(bucket_name=GCS_BUCKET, object_name=GCS_OBJECT)
            df = pd.read_csv(io.BytesIO(file_bytes))
            return df.to_json(orient="records")

        api_data = extract_from_api()
        pg_data = extract_from_postgres()
        gcs_data = file_sensor >> extract_from_gcs()

    # ------------------------
    # 🚀 LOAD GROUP
    # ------------------------
    with TaskGroup("LOAD_INTO_BIGQUERY", tooltip="Load raw data into BigQuery") as load_group:

        @task
        def load_to_bq(json_data, table_name):
            dataset = BQ_DATASET
            client = bigquery.Client(project=GCP_PROJECT_ID)
            table_id = f"{GCP_PROJECT_ID}.{dataset}.{table_name}"

            df = pd.read_json(io.StringIO(json_data))

            # Convert DataFrame to JSON bytes and upload directly to BigQuery
            buffer = io.BytesIO()
            df.to_json(buffer, orient="records", lines=True)
            buffer.seek(0)

            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                autodetect=True,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
            )

            load_job = client.load_table_from_file(buffer, table_id, job_config=job_config)
            load_job.result()

            print(f"✅ Loaded data into {table_id}")
            return table_id

        load_products = load_to_bq.override(task_id="load_products")(gcs_data, BQ_TABLE_ECOM_PRODUCTS)
        load_orders = load_to_bq.override(task_id="load_orders")(api_data, BQ_TABLE_ECOM_ORDERS)
        load_customers = load_to_bq.override(task_id="load_customers")(pg_data, BQ_TABLE_ECOM_CUSTOMERS)

    # ------------------------
    # 🔧 TRANSFORM GROUP
    # ------------------------
    with TaskGroup("TRANSFORM_USING_DBT", tooltip="Run dbt transformations") as transform_group:
        @task()
        def run_dbt_models():
            print("Running dbt models (staging -> marts)...")
            cmd = ["dbt", "build", "--project-dir", DBT_PROJECT_DIR, "--profiles-dir", DBT_PROFILES_DIR, "-s", "+mart_ecom_sales_summary"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.returncode != 0:
                print(result.stderr)
                raise Exception("dbt run failed")
            return "Successfully built and tested dbt models"
        run_dbt_models()

    # DAG Dependencies
    gcs_data >> load_products
    api_data >> load_orders
    pg_data >> load_customers

    [load_products, load_orders, load_customers] >> transform_group


elt_ecommerce()
