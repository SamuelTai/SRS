from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
from sqlalchemy import create_engine
import logging

def load_csv_to_postgres():
    try:
        # Database connection string
        db_url = 'postgresql+psycopg2://user:password@postgres_db/property_db'
        engine = create_engine(db_url)

        # Log connection success
        logging.info("Connected to the PostgreSQL database.")

        # Load CSV data into a DataFrame
        csv_path = '/opt/airflow/dags/data/properties_data.csv'
        df = pd.read_csv(csv_path)
        logging.info(f"CSV data loaded successfully. Number of records: {len(df)}")

        # Write DataFrame to PostgreSQL
        df.to_sql('properties', engine, if_exists='replace', index=False)
        logging.info("Data loaded into the 'properties' table successfully.")
    
    except Exception as e:
        logging.error(f"Failed to load CSV to PostgreSQL: {e}")
        raise

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'load_csv_to_postgres',
    default_args=default_args,
    description='A simple ETL pipeline to load CSV into PostgreSQL',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    load_csv_task = PythonOperator(
        task_id='load_csv',
        python_callable=load_csv_to_postgres,
    )
