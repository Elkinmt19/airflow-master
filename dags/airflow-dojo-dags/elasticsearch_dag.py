# Built-in imports
from datetime import datetime

# Airflow imports
from airflow import DAG
from elasticsearch_plugin.hooks.elastic_hook import ElasticHook
from airflow.operators.python import PythonOperator
from plugins.elasticsearch_plugin.operators.postgres_to_elastic import PostgresToElasticOperator

default_args = {
    "start_date": datetime(2020,1,1)
}

def _print_es_info():
    hook = ElasticHook()
    print(hook.info())

with DAG(
    "elasticsearch_dag",
    schedule_interval="@daily",
    default_args=default_args,
    tags=["airflow-dojo-dags","Testing"],
    catchup=False
) as dag:

    print_es_info = PythonOperator(
        task_id="print_es_info",
        python_callable=_print_es_info
    )

    connections_to_es = PostgresToElasticOperator(
        task_id="connections_to_es",
        sql="SELECT * FROM connection",
        index="connections"
    )

    print_es_info >> connections_to_es