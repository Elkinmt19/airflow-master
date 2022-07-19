# Built-in imports
from datetime import datetime

# Airflow imports
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from airflow.utils.task_group import TaskGroup

default_args = {
    "start_date": datetime(2020,1,1)
}


with DAG(
    'parallel_dag_task_group', 
    default_args=default_args, 
    schedule_interval='@daily',
    tags=["airflow-dojo-dags","Testing"],
    catchup=False
) as dag:

    extract_a = BashOperator(
        task_id='extract_a',
        bash_command='sleep 1'
    )

    extract_b = BashOperator(
        task_id='extract_b',
        bash_command='sleep 1'
    )

    with TaskGroup("processing_tasks") as processing_tasks:
        load_a = BashOperator(
            task_id='load_a',
            bash_command='sleep 1'
        )

        load_b = BashOperator(
            task_id='load_b',
            bash_command='sleep 1'
        )

    transform = BashOperator(
        task_id='transform',
        bash_command='sleep 1'
    )

    extract_a >> processing_tasks
    extract_b >> processing_tasks
    processing_tasks >> transform