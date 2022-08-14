from pyspark.sql import SparkSession

spark = SparkSession.\
        builder.\
        appName("liverpool-players-analysis").\
        master("spark://spark-master:7077").\
        config("spark.executor.memory", "512m").\
        getOrCreate()

liverpool_players = spark.read.csv(
    path="/opt/airflow/tmp_files/liverpool_players.csv", sep=",", header=True
)

top_scorers_pl = spark.read.csv(
    path="/opt/airflow/tmp_files/top_scorers_pl.csv",sep=",", header=True
)

top_liverpool_scorers = liverpool_players.alias("lp").join(
    top_scorers_pl.alias("ts"),
    ['id'],
    "inner"
).select(
    "lp.id",
    "ts.name",
    "ts.firstName",
    "ts.lastName",
    "ts.dateOfBirth",
    "ts.nationality",
    "ts.position"
)

top_liverpool_scorers.write.csv("/opt/airflow/tmp_files/top_liverpool_scorers")