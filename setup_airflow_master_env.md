# <img src="./assets/imgs/airflow.png"  width="5%"/> **Setup the Airflow Master Work Environment** <img src="./assets/imgs/airflow.png"  width="5%"/>

In order to be able to work and run all of the projects in this repo, it is necessary to setup an environment first with all the dependencies and modules needed. In order to de this you must follow the steps below:

- Create a file call `.env` at the same level of the repository directory, then you just have to put the following lines of code in it:

    ```bash 
    AIRFLOW_IMAGE_NAME=apache/airflow:2.3.0
    AIRFLOW_UID=50000
    ```

- Then the last step to finish this setup is run the `docker-compose.yml` file, which contains all the instructions and container configuration needed to correctly install Airflow. To run the docker-compose file you just have to run the following command:
    ```bash 
    docker-compose up -d
    ```
Now everything is setup and ready to stark working with airflow in this repository.