# Built-in imports
from datetime import datetime

# Airflow imports
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator

# Own imports
from subdags.subdag_parallenl_dag import subdag_parallel_dag

default_args = {
    "start_date": datetime(2020,1,1)
}


with DAG(
    'parallel_dag_subdag',
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

    processing = SubDagOperator(
        task_id="processing_tasks",
        subdag=subdag_parallel_dag("parallel_dag","processing_tasks", default_args)
    )

    transform = BashOperator(
        task_id='transform',
        bash_command='sleep 1'
    )

    extract_a >> processing
    extract_b >> processing
    processing >> transform