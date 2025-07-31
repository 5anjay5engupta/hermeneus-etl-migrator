from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from datetime import datetime
import csv

# Define a function to read from the CSV file
def read_csv(**kwargs):
    ti = kwargs['ti']
    file_path = '/data/source/customer.csv'
    data = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    ti.xcom_push(key='customer_data', value=data)

# Define a function to transform the data
def transform_data(**kwargs):
    ti = kwargs['ti']
    customer_data = ti.xcom_pull(key='customer_data', task_ids='read_csv_task')
    transformed_data = []
    for row in customer_data:
        full_name = f"{row['first_name']} {row['last_name']}"
        load_date = datetime.now()
        transformed_data.append({
            'customer_id': row['customer_id'],
            'full_name': full_name,
            'email': row['email'],
            'load_date': load_date
        })
    ti.xcom_push(key='transformed_data', value=transformed_data)

# Define a function to load data into MySQL
def load_to_mysql(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(key='transformed_data', task_ids='transform_data_task')
    mysql_hook = MySqlHook(mysql_conn_id='mysql_default')
    insert_query = """
    INSERT INTO customer_dw (customer_id, full_name, email, load_date)
    VALUES (%s, %s, %s, %s)
    """
    for row in transformed_data:
        mysql_hook.run(insert_query, parameters=(row['customer_id'], row['full_name'], row['email'], row['load_date']))

# Define the DAG
with DAG(
    dag_id='talend_to_airflow_migration',
    schedule_interval='@daily',
    start_date=datetime(2023, 10, 1),
    catchup=False,
    description='A simple ETL DAG converted from Talend to Airflow',
) as dag:

    # Task to read CSV
    read_csv_task = PythonOperator(
        task_id='read_csv_task',
        python_callable=read_csv,
        provide_context=True
    )

    # Task to transform data
    transform_data_task = PythonOperator(
        task_id='transform_data_task',
        python_callable=transform_data,
        provide_context=True
    )

    # Task to load data into MySQL
    load_to_mysql_task = PythonOperator(
        task_id='load_to_mysql_task',
        python_callable=load_to_mysql,
        provide_context=True
    )

    # Set task dependencies
    read_csv_task >> transform_data_task >> load_to_mysql_task
```