# Built-in imports
from datetime import datetime, timedelta

# External imports
import requests
import pandas as pd

# Airflow imports
from airflow import DAG
from airflow.sensors.http_sensor import HttpSensor
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from airflow.operators.email_operator import EmailOperator

default_args = {
    "owner": "Elkinmt19",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "elkinmt19@gmail.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}


HEADERS = { "X-Auth-Token": Variable.get("X-Auth-Token", deserialize_json=True) }

def _top_liverpool_scorers_processing():
    liverpool_players = pd.read_csv("/opt/airflow/tmp_files/liverpool_players.csv")
    top_scorers_pl = pd.read_csv("/opt/airflow/tmp_files/top_scorers_pl.csv")

    top_liverpool_scorers = pd.merge(liverpool_players, top_scorers_pl, on="id", how="inner")[[
        "id","name_y","firstName","lastName","dateOfBirth_y","nationality_y","position_y"
    ]].rename(columns={
        "name_y":"name","dateOfBirth_y":"dateOfBirth","nationality_y":"nationality","position_y":"position"
    })

    top_liverpool_scorers.to_html(
        "/opt/airflow/tmp_files/top_liverpool_scorers.html",
        index=False
    )


def _fetch_top_scorers_premier_league():
    URI = 'https://api.football-data.org/v4/competitions/PL/scorers/?season=2021'

    response = requests.get(URI, headers=HEADERS)

    top_scorers_json = []

    for scorer in response.json()["scorers"]:
        top_scorers_json.append(scorer["player"])

    pd.DataFrame(top_scorers_json).to_csv(
        "/opt/airflow/tmp_files/top_scorers_pl.csv",
        index=False
    )

def _fetch_liverpool_players():
    URI = 'https://api.football-data.org/v4/teams/64/?season=2021'

    response = requests.get(URI, headers=HEADERS)

    liverpool_players_json = response.json()["squad"]

    pd.DataFrame(liverpool_players_json).to_csv(
        "/opt/airflow/tmp_files/liverpool_players.csv",
        index=False
    )

with DAG(
    dag_id="scorers_liverpool_players",
    start_date=datetime(2022,8,1),
    schedule_interval="@daily",
    default_args=default_args,
    tags=["airflow_vs_step_functions"],
    catchup=False
) as dag:

    is_top_scorers_premier_league_available = HttpSensor(
        task_id="is_top_scorers_premier_league_available",
        method="GET",
        http_conn_id="football_data_api",
        endpoint="competitions/PL/scorers/?season=2021",
        response_check=lambda response: f"Status Code: {response.status_code}",
        poke_interval=5,
        timeout=20
    )

    is_liverpool_players_available = HttpSensor(
        task_id="is_liverpool_players_available",
        method="GET",
        http_conn_id="football_data_api",
        endpoint="teams/64/?season=2021",
        response_check=lambda response: f"Status Code: {response.status_code}",
        poke_interval=5,
        timeout=20
    )

    fetch_top_scorers_premier_league = PythonOperator(
        task_id="fetch_top_scorers_premier_league",
        python_callable=_fetch_top_scorers_premier_league
    )

    fetch_liverpool_players = PythonOperator(
        task_id="fetch_liverpool_players",
        python_callable=_fetch_liverpool_players
    )

    top_liverpool_scorers_processing = PythonOperator(
        task_id="top_liverpool_scorers_processing",
        python_callable=_top_liverpool_scorers_processing
    )

    is_top_scorers_premier_league_available >> fetch_top_scorers_premier_league
    is_liverpool_players_available >> fetch_liverpool_players
    [fetch_top_scorers_premier_league, fetch_liverpool_players] >> top_liverpool_scorers_processing