from __future__ import annotations
import json
from textwrap import dedent
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.DimondPricePrediction.pipelines.training_pipeline import TrainingPipeline
import os
import boto3

training_pipeline = TrainingPipeline()

with DAG(
    "gemstone_training_pipeline",
    default_args={"retries": 2},
    description="it is my training pipeline",
    schedule="@weekly",  # here you can test based on hour or mints but make sure here you container is up and running
    start_date=pendulum.datetime(2024, 1, 17, tz="UTC"),
    catchup=False,
    tags=["machine_learning ", "classification", "gemstone"],
) as dag:

    dag.doc_md = __doc__

    def data_ingestion(**kwargs):
        ti = kwargs["ti"]
        train_data_path, test_data_path = training_pipeline.start_data_ingestion()
        ti.xcom_push(
            "data_ingestion_artifact",
            {"train_data_path": train_data_path, "test_data_path": test_data_path},
        )
    
    # Define the function before it is called
    def push_data_to_s3(**kwargs):
        # Your implementation for pushing data to S3
        pass

    def push_model_to_s3(**kwargs):
    # Ottieni il percorso del modello dalla XCom
        ti = kwargs["ti"]
        model_path = ti.xcom_pull(task_ids="model_trainer", key="model_path")

        # Configura le credenziali e la sessione di AWS
        aws_access_key_id = "YOUR_ACCESS_KEY_ID"
        aws_secret_access_key = "YOUR_SECRET_ACCESS_KEY"
        region_name = "YOUR_REGION_NAME"
        bucket_name = "YOUR_BUCKET_NAME"

        # Inizializza il client S3
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        # Carica il file del modello sul bucket S3
        model_name = os.path.basename(model_path)
        s3_client.upload_file(model_path, bucket_name, model_name)

        print("Model uploaded to S3 successfully!")

    def data_transformations(**kwargs):
        ti = kwargs["ti"]
        data_ingestion_artifact = ti.xcom_pull(
            task_ids="data_ingestion", key="data_ingestion_artifact"
        )
        train_arr, test_arr = training_pipeline.start_data_transformation(
            data_ingestion_artifact["train_data_path"],
            data_ingestion_artifact["test_data_path"],
        )
        train_arr = train_arr.tolist()
        test_arr = test_arr.tolist()
        ti.xcom_push(
            "data_transformations_artifcat",
            {"train_arr": train_arr, "test_arr": test_arr},
        )

    def model_trainer(**kwargs):
        import numpy as np

        ti = kwargs["ti"]
        data_transformation_artifact = ti.xcom_pull(
            task_ids="data_transformation", key="data_transformations_artifcat"
        )
        train_arr = np.array(data_transformation_artifact["train_arr"])
        test_arr = np.array(data_transformation_artifact["test_arr"])
        training_pipeline.start_model_training(train_arr, test_arr)

    data_ingestion_task = PythonOperator(
        task_id="data_ingestion",
        python_callable=data_ingestion,
    )

    data_ingestion_task.doc_md = dedent(
        """\
    #### Ingestion task
    this task creates a train and test file.
    """
    )

    data_transform_task = PythonOperator(
        task_id="data_transformation",
        python_callable=data_transformations,
    )

    data_transform_task.doc_md = dedent(
        """\
    #### Transformation task
    this task performs the transformation
    """
    )

    model_trainer_task = PythonOperator(
        task_id="model_trainer",
        python_callable=model_trainer,
    )
    model_trainer_task.doc_md = dedent(
        """\
    #### model trainer task
    this task perform training
    """
    )

    push_data_to_s3_task = PythonOperator(
        task_id="push_data_to_s3",
        python_callable=push_data_to_s3
    )


data_ingestion_task >> data_transform_task >> model_trainer_task >> push_data_to_s3_task
