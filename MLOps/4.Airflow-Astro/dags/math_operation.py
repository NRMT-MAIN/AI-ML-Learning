"""
Math Pipeline DAG

Task 1: Start with an initial number: 10
Task 2: Add 5
Task 3: Multiply by 2
Task 4: Subtract 3
Task 5: Compute square

Final calculation:
10 -> 15 -> 30 -> 27 -> 729
"""

# Import DAG to define an Airflow workflow
from airflow import DAG

# Import PythonOperator to execute Python functions as Airflow tasks
from airflow.providers.standard.operators.python import PythonOperator

# Import datetime to define the DAG start date
from datetime import datetime


# -------------------------------
# Task 1: Start Number
# -------------------------------
def start_number(**context):
    # Define the initial number
    number = 10

    # Push the value to XCom so the next task can access it
    context["task_instance"].xcom_push(
        key="current_value",
        value=number
    )

    # Print the starting number in task logs
    print(f"Starting number: {number}")


# -------------------------------
# Task 2: Add Five
# -------------------------------
def add_five(**context):
    # Pull the number pushed by the previous task: start_number
    number = context["task_instance"].xcom_pull(
        key="current_value",
        task_ids="start_number"
    )

    # Add 5 to the pulled number
    number += 5

    # Push the updated value to XCom for the next task
    context["task_instance"].xcom_push(
        key="current_value",
        value=number
    )

    # Print the result in task logs
    print(f"Number after adding 5: {number}")


# -------------------------------
# Task 3: Multiply By Two
# -------------------------------
def multiply_by_two(**context):
    # Pull the number pushed by add_five task
    number = context["task_instance"].xcom_pull(
        key="current_value",
        task_ids="add_five"
    )

    # Multiply the number by 2
    number *= 2

    # Push the updated value to XCom for the next task
    context["task_instance"].xcom_push(
        key="current_value",
        value=number
    )

    # Print the result in task logs
    print(f"Number after multiplying by 2: {number}")


# -------------------------------
# Task 4: Subtract Three
# -------------------------------
def subtract_three(**context):
    # Pull the number pushed by multiply_by_two task
    number = context["task_instance"].xcom_pull(
        key="current_value",
        task_ids="multiply_by_two"
    )

    # Subtract 3 from the number
    number -= 3

    # Push the updated value to XCom for the next task
    context["task_instance"].xcom_push(
        key="current_value",
        value=number
    )

    # Print the result in task logs
    print(f"Number after subtracting 3: {number}")


# -------------------------------
# Task 5: Compute Square
# -------------------------------
def compute_square(**context):
    # Pull the number pushed by subtract_three task
    number = context["task_instance"].xcom_pull(
        key="current_value",
        task_ids="subtract_three"
    )

    # Compute square of the number
    number **= 2

    # Push final result to XCom
    context["task_instance"].xcom_push(
        key="current_value",
        value=number
    )

    # Print final result in task logs
    print(f"Final result: {number}")


# -------------------------------
# Define the DAG
# -------------------------------
with DAG(
    # Unique DAG ID shown in Airflow UI
    dag_id="math_pipeline",

    # Airflow starts scheduling the DAG from this date
    start_date=datetime(2024, 6, 1),

    # Run this DAG once every day
    schedule="@daily",

    # Prevent Airflow from creating old missed runs
    catchup=False
) as dag:

    # Task 1: Start with number 10
    task1 = PythonOperator(
        task_id="start_number",
        python_callable=start_number
    )

    # Task 2: Add 5 to previous number
    task2 = PythonOperator(
        task_id="add_five",
        python_callable=add_five
    )

    # Task 3: Multiply previous result by 2
    task3 = PythonOperator(
        task_id="multiply_by_two",
        python_callable=multiply_by_two
    )

    # Task 4: Subtract 3 from previous result
    task4 = PythonOperator(
        task_id="subtract_three",
        python_callable=subtract_three
    )

    # Task 5: Square the final value
    task5 = PythonOperator(
        task_id="compute_square",
        python_callable=compute_square
    )

    # Define execution order:
    # start_number -> add_five -> multiply_by_two -> subtract_three -> compute_square
    task1 >> task2 >> task3 >> task4 >> task5