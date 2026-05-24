from airflow import DAG
from airflow.decorators import task
from datetime import datetime


## task flow API approach : Here we will use the @task decorator to define our tasks as functions,
##  and Airflow will handle the dependencies automatically based on the order of function calls.

# Define the DAG
with DAG(
    dag_id='taskflow_api_example',
    start_date=datetime(2024, 6, 1),
    schedule='@daily',
    catchup=False
) as dag:
    @task
    def start_task():
        initial_value = 5
        print(f"Initial value: {initial_value}")
        return initial_value # This value will be passed to the next task automatically by Airflow
    
    @task
    def multiply_by_two(number):
        result = number * 2
        print(f"After multiplying by 2: {result}")
        return result
    
    @task
    def subtract_three(number):
        result = number - 3
        print(f"After subtracting 3: {result}")
        return result
    
    @task
    def compute_square(number):
        result = number ** 2
        print(f"Final result (square): {result}")
        return result
    
    # Define the task dependencies by calling the tasks in sequence
    initial_value = start_task()
    multiplied_value = multiply_by_two(initial_value)
    subtracted_value = subtract_three(multiplied_value)
    final_result = compute_square(subtracted_value)
    # The final_result will be the output of the last task in the sequence, and it will be printed in the logs.
