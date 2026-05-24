from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

## Define our task 1
def preprocess_data() : 
    print("Preprocessing data...")

## Define our task 2
def train_model() :
    print("Training model...")

## Define our task 3
def evaluate_model() :
    print("Evaluating model...")

## Define the DAG
with DAG(
    'ml_pipeline',
    start_date=datetime(2024, 6, 1),
    schedule='@daily'
) as dag :
    
    task1 = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data
    )

    task2 = PythonOperator(
        task_id='train_model',
        python_callable=train_model
    )

    task3 = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model
    )

    ## Set the task dependencies
    task1 >> task2 >> task3     
