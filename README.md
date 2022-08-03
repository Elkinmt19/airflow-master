#  <img src="./assets/imgs/airflow.png"  width="5%"/> **AIRFLOW MASTER**  <img src="./assets/imgs/airflow.png"  width="5%"/>

This repository contains some small projects related to the field of Data Engineering and Machine Learning Engineering. Here `Airflow` is used as the main workflow orchestrator tool in order to build, develop and deploy different Data and ML pipelines into production environments.

<p align="center">
    <img src="assets/imgs/airflow_logo.png" width="40%"/>
    <img src="assets/imgs/data_pipeline.avif" width="50%"/>
</p>


## Software Dependencies :computer:
* [Python](https://www.python.org/) <br>
Python is a programming language that lets you work quickly and integrate systems more effectively.  
* [Docker](https://www.docker.com/) <br>
Docker is an open-source project for automating the deployment of applications as portable, self-sufficient containers that can run on the cloud or on-premises.
* [Docker-compose](https://docs.docker.com/compose/) <br>
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services.


## Author
## Elkin Javier Guerra Galeano <img src="./assets/imgs/robotboy_fly.gif"/>

Machine Learning Engineer, passionate about artificial intelligence and software development, I am currently exploring the world of MLOps, researching and gaining more and more knowledge on this topic. I am very interested in cloud computing and currently have experience working with AWS and GCP. 🐨 🚀

## Getting Started

In order to start running the projects of this repo, first you must check the [Setup Guide](./setup_airflow_master_env.md) of these repo, which are a couple of steps that you need to follow in order to setup a working environment to run the projects of this repo.

Once you have completed those steps, you can go to your web browser and go to `http://localhost:8080` to interact with the Airflow's UI.

To sign in you must use the following credentials:

- Username: airflow
- Password: airflow

Now you can start exploring the Airflow's UI and working with Airflow in your Data workflows!!!

## Best Practices
The best practices are important in everything and of course when you're working with Airflow this is'nt any different. Some of the most common best practices in airflow are the followings:

- Always test your tasks one by one before test the whole Data Pipeline.
    - One efficient way to test a single task of a DAG is using the airflow's command line.

- Test your DAG's locally before jump into production environments.
    - This task can be achieve using the Airflow's command line.

## Airflow CLI commands
In order to be able to use the Airflow's command line, you first have to create a session into the docker container that runs the scheduler of our Airflow's installation, to do that you just have to run the following command:

```bash 
docker exec -it airflow-master_airflow-scheduler_1 /bin/bash
``` 
Now that you're inside the docker container, you can start using and testing the Airflow's CLI commands.

Some useful commands are the following:

- In order to list all the DAG's available, run the following command:
    ```bash
    airflow dags list
    ```

- To run a single tasks of a specific DAG, run the following command:
    ```bash
    airflow tasks test <dag_id> <task_id> <execution_date> (format='year-month-day')
    ```

- To trigger a DAG run of a specific DAG, use the following command:
    ```bash
    airflow dags trigger <dag_id>
    ```
