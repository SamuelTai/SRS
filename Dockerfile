FROM apache/airflow:2.7.2-python3.8

USER root
RUN pip install pandas psycopg2-binary

USER airflow