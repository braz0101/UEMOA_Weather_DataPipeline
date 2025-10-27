from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys, os, logging
import pandas as pd
import psycopg2

scripts_path = '/opt/airflow/scripts'
if scripts_path not in sys.path:
    sys.path.append(scripts_path)

from etl_meteo import fetch_weather_current_hour, insert_into_db, export_to_csv, REGIONS, HOURLY_VARIABLES

default_args = {
    'owner': 'ibrahima',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='meteo_uemoa_hourly',
    default_args=default_args,
    description='ETL météo UEMOA chaque heure - pipeline détaillé',
    schedule_interval='@hourly',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['meteo', 'uemoa'],
)

TEMP_DATA_PATH = "/opt/airflow/exports/temp_data.parquet"
CSV_EXPORT_PATH = "/opt/airflow/exports/meteo_uemoa.csv"

def collect_data(**context):
    all_records = []
    for pays, regions in REGIONS.items():
        for region in regions:
            logging.info(f"Collecte {region['nom']}")
            data = fetch_weather_current_hour(region['latitude'], region['longitude'])
            if data:
                record = {
                    "pays": pays,
                    "region": region['nom'],
                    "latitude": region['latitude'],
                    "longitude": region['longitude'],
                    "altitude": region['altitude'],
                    "observation_time": data['time'],
                }
                for var in HOURLY_VARIABLES:
                    record[var] = data.get(var)
                all_records.append(record)
    if all_records:
        df = pd.DataFrame(all_records)
        df.to_parquet(TEMP_DATA_PATH, index=False)
        logging.info(f"{len(all_records)} enregistrements stockés temporairement.")
    else:
        logging.warning("Aucune donnée collectée")

def insert_data(**context):
    if not os.path.exists(TEMP_DATA_PATH):
        logging.warning("Fichier temporaire absent, insertion annulée")
        return
    df = pd.read_parquet(TEMP_DATA_PATH)
    conn = psycopg2.connect(dbname="climat_uemoa", user="postgres", password="passer", host="host.docker.internal",
    port=5433)
    conn.autocommit = True
    for _, row in df.iterrows():
        insert_into_db(conn, row.to_dict())
    conn.close()
    logging.info(f"Insertion en base terminée pour {len(df)} enregistrements.")

def export_data(**context):
    if not os.path.exists(TEMP_DATA_PATH):
        logging.warning("Fichier temporaire absent, export annulé")
        return
    df = pd.read_parquet(TEMP_DATA_PATH)
    try:
        export_to_csv(df, CSV_EXPORT_PATH)
        logging.info(f"Export CSV finalisé avec succès.")
    finally:
        os.remove(TEMP_DATA_PATH)
        logging.info("Fichier temporaire supprimé.")

task_collect = PythonOperator(
    task_id='collect_data',
    python_callable=collect_data,
    dag=dag
)

task_insert = PythonOperator(
    task_id='insert_data',
    python_callable=insert_data,
    dag=dag
)

task_export = PythonOperator(
    task_id='export_data',
    python_callable=export_data,
    dag=dag
)

task_collect >> task_insert >> task_export
