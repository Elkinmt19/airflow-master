# Built-in imports
from random import uniform
from datetime import datetime

# External imports
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup


default_args = {
    'start_date': datetime(2020, 1, 1)
}

def _training_model(ti):
    accuracy = uniform(0.1, 10.0)
    print(f'model\'s accuracy: {accuracy}')
    ti.xcom_push(key="model_accuracy", value=accuracy)

def _choose_best_model(ti):
    print('choose best model')
    accuracies = ti.xcom_pull(key="model_accuracy", task_ids=[
        "processing_tasks.training_model_a",
        "processing_tasks.training_model_b",
        "processing_tasks.training_model_c"
    ])
    print(accuracies)

with DAG(
    'xcom_dag',
    schedule_interval='@daily',
    default_args=default_args,
    tags=["airflow-dojo-dags","Testing"],
    catchup=False
) as dag:

    downloading_data = BashOperator(
        task_id='downloading_data',
        bash_command='sleep 3',
        do_xcom_push=False
    )

    with TaskGroup('processing_tasks') as processing_tasks:
        training_model_a = PythonOperator(
            task_id='training_model_a',
            python_callable=_training_model
        )

        training_model_b = PythonOperator(
            task_id='training_model_b',
            python_callable=_training_model
        )

        training_model_c = PythonOperator(
            task_id='training_model_c',
            python_callable=_training_model
        )

    choose_model = PythonOperator(
        task_id='task_4',
        python_callable=_choose_best_model
    )

    downloading_data >> processing_tasks >> choose_model