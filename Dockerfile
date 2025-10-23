FROM astrocrpublic.azurecr.io/runtime:3.1-2

RUN pip install dbt-bigquery

# Copy GCP key into the Airflow container
COPY include/keys/gcp_bq_key.json /usr/local/airflow/include/keys/gcp_bq_key.json

# USER root
# RUN apt-get update && apt-get install -y git

# USER airflow

# Install dbt and Google providers
# RUN pip install dbt-bigquery google-cloud-bigquery google-cloud-storage
