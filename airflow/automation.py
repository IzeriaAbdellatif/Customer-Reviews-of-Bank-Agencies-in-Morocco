import subprocess
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

folder = "/home/aizeria/Documents/work/Customer-Reviews-of-Bank-Agencies-in-Morocco"

def extract_data_task():
    script_path = f"{folder}/data extraction/ingestion_scripts/extract_json_data.py"
    try:
        print(f"Attempting to execute: {script_path}")
        print(f"Python path: {sys.executable}")

        process = subprocess.Popen(
            [sys.executable, script_path],
            cwd=folder,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # Line-buffered
        )

        # Stream output line-by-line
        for line in process.stdout:
            print(line, end='')

        process.wait()

        if process.returncode != 0:
            raise Exception(f"Script failed with code {process.returncode}")

    except Exception as e:
        print(f"Critical error: {str(e)}")
        raise


def load_data_task():
    script_path = f"{folder}/data loading & enrichment/bank_branches.py"
    try:
        print(f"Attempting to execute: {script_path}")
        print(f"Python path: {sys.executable}")

        process = subprocess.Popen(
            [sys.executable, script_path],
            cwd=f"{folder}",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # Line-buffered
        )

        # Stream output line-by-line
        for line in process.stdout:
            print(line, end='')

        process.wait()

        if process.returncode != 0:
            raise Exception(f"Script failed with code {process.returncode}")

    except Exception as e:
        print(f"Critical error: {str(e)}")
        raise


def transform_data_task():
    dbt_project_path = f"{folder}/data_transformation_with_dbt"
    try:
        print(f"Running dbt in: {dbt_project_path}")
        print(f"Python path: {sys.executable}")

        process = subprocess.Popen(
            ["dbt", "run"],
            cwd=dbt_project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            print(line, end='')

        process.wait()

        if process.returncode != 0:
            raise Exception(f"dbt run failed with exit code {process.returncode}")

    except Exception as e:
        print(f"Critical error during dbt run: {str(e)}")
        raise



dag = DAG(
    dag_id='Customer-Reviews-of-bank-Agencies-in-Morocco-dag',
    description='A DAG for customer reviews.',
    schedule_interval='@monthly',  # Run daily
    start_date=datetime(2025, 5, 7),  # Start date
    catchup=False,  # Don't run previous missed instances
)

task1 = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_task,
    dag=dag
)

task2 = PythonOperator(
    task_id='load_data',
    python_callable=load_data_task,
    dag=dag
)

task3 = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data_task,
    dag=dag
)


task1 >> task2 >> task3