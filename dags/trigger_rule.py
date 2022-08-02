# Built-in imports
from datetime import datetime 

# External imports
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "start_date": datetime(2020,1,1)
}

with DAG(
    "trigger_rule",
    schedule_interval="@daily",
    default_args=default_args,
    tags=["airflow-dojo-dags","Testing"],
    catchup=False
) as dag:
    task_1 = BashOperator(
        task_id="task_1",
        bash_command="exit 0",
        do_xcom_push=False
    )

    task_2 = BashOperator(
        task_id="task_2",
        bash_command="exit 0",
        do_xcom_push=False
    )

    task_3 = BashOperator(
        task_id="task_3",
        bash_command="exit 0",
        do_xcom_push=False,
        trigger_rule="one_failed"
    )

    [task_1,task_2] >> task_3