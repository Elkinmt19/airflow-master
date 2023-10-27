import os
from typing import Union, Any, Dict
from airflow.decorators import dag, task
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction import DictVectorizer
import logging
import pandas as pd

logger = logging.getLogger("airflow.task")

def prepare_features(
    df:pd.DataFrame, 
    categorical:str, train=True
) -> pd.DataFrame:
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        logger.info(f"The mean duration of training is {mean_duration}")
    else:
        logger.info(f"The mean duration of validation is {mean_duration}")
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def train_model(
    df:pd.DataFrame, 
    categorical:str
) -> Union[LinearRegression, DictVectorizer, float]:
    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    logger.info(f"The shape of X_train is {X_train.shape}")
    logger.info(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    rmse = mean_squared_error(y_train, y_pred, squared=False)
    logger.info(f"The RMSE of training is: {rmse}")

    return lr, dv, rmse

def run_model(
    df:pd.DataFrame,
    categorical:str, 
    dv:DictVectorizer, 
    lr:LinearRegression
) -> Union[bool, float]:
    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    rmse = mean_squared_error(y_val, y_pred, squared=False)
    logger.info(f"The RMSE of validation is: {rmse}")

    return True, rmse

default_args = {
    "owner": "Elkinmt19",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "elkinmt19@gmail.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

@dag(
    dag_id="fhv_ml_model_training",
    start_date=datetime(2023,9,1),
    schedule_interval="@monthly",
    default_args=default_args,
    tags=["machine-learning"],
    catchup=False
) 
def taskflow():
    @task(task_id="get_paths_data", multiple_outputs=True)
    def get_paths() -> Union[str, str]:
        logger.info("Getting the train and validation datasets...")

        train_path = os.path.join(
            "https://d37ci6vzurychx.cloudfront.net/trip-data/",
            f"fhv_tripdata_{str(date.today() - relativedelta(months=4))[:-3]}.parquet"
        )
        val_path = os.path.join(
            "https://d37ci6vzurychx.cloudfront.net/trip-data/",
            f"fhv_tripdata_{str(date.today() - relativedelta(months=3))[:-3]}.parquet"
        )
        logger.info("The dataset path's were gotten properly!!!")

        return {"train_path": train_path, "val_path": val_path}
    
    @task(task_id="build_machine_learning_model", multiple_outputs=True)
    def build_machine_learning_model(paths: Dict[str, str]):
        logger.info("Loading the train and validation datasets...")
        df_train = pd.read_parquet(paths["train_path"])
        df_val = pd.read_parquet(paths["val_path"])
        logger.info("The datasets were loaded properly!!!")

        categorical = ['PUlocationID', 'DOlocationID']

        logger.info("Pre-processing the train and validation datasets...")
        df_train_processed = prepare_features(df_train, categorical)
        df_val_processed = prepare_features(df_val, categorical, False)
        logger.info("The datasets were preprocessed properly!!!")

        logger.info("Start the training of the model...")
        lr, dv, train_rmse = train_model(df_train_processed, categorical)
        _ ,val_rmse = run_model(df_val_processed, categorical, dv, lr)
        logger.info("The model was trained properly!!!")

        return {"train_rmse": train_rmse, "val_rmse": val_rmse}

    build_machine_learning_model(get_paths())
        

taskflow()