from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Chemin vers les scripts
scripts_path = '/opt/airflow/scripts'
if scripts_path not in sys.path:
    sys.path.append(scripts_path)

# Import des fonctions spécifiques
try:
    from update_dimensions_facts import update_dimensions_facts
except ImportError as e:
    print(f"[DAG LOAD ERROR] Impossible d'importer update_dimensions_facts : {e}")
    raise

# Paramètres des tâches
default_args = {
    'owner': 'ibrahima',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}

# Définition du DAG
with DAG(
    dag_id='update_dimensions_facts',
    default_args=default_args,
    description='Mise à jour en 3 étapes : dimension_date, fact_meteo, confirmation',
    schedule_interval='30 * * * *',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['meteo', 'update'],
) as dag:

    # Bloc 1 : Mise à jour de la dimension_date seule
    def update_dim_date():
        from update_dimensions_facts import update_dimensions_facts
        # Tu modifies ton script pour que la fonction accepte un paramètre
        update_dimensions_facts(cible='dimension_date')

    update_date_task = PythonOperator(
        task_id='update_dimension_date',
        python_callable=update_dim_date
    )

    # Bloc 2 : Mise à jour des faits météo
    def update_fact_meteo():
        from update_dimensions_facts import update_dimensions_facts
        update_dimensions_facts(cible='fact_meteo')

    update_facts_task = PythonOperator(
        task_id='update_fact_meteo',
        python_callable=update_fact_meteo
    )

    # Bloc 3 : Tâche finale pour confirmation
    def fin_processus():
        print("Mise à jour terminée avec succès.")

    fin_task = PythonOperator(
        task_id='confirmation_finale',
        python_callable=fin_processus
    )

    # Dépendances : on enchaîne les blocs
    update_date_task >> update_facts_task >> fin_task
