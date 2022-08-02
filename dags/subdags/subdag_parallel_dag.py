# Airflow imports
from airflow import DAG
from airflow.operators.bash import BashOperator

def subdag_parallel_dag(parent_dag_id, child_dag_id, default_args):
    with DAG(dag_id=f"{parent_dag_id}.{child_dag_id}", default_args=default_args) as dag:
        load_a = BashOperator(
            task_id='load_a',
            bash_command='sleep 1'
        )

        load_b = BashOperator(
            task_id='load_b',
            bash_command='sleep 1'
        )

        return dag