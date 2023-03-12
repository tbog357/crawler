from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

from data_cleaner import data_cleaner

default_args = {
    "owner": "Airflow",
    "start_date": datetime(2022, 3, 5),
    "retries": 1,
    "retry_delay": timedelta(seconds=5),
}

dag = DAG(
    "store_dag",
    default_args=default_args,
    schedule_interval="@daily",
    template_searchpath=['/sql_files'],
    catchup=False,
)

t1 = BashOperator(
    task_id="check_file_exists",
    bash_command="shasum /store_files/raw_store_transactions.csv",
    retries=2,
    retry_delay=timedelta(seconds=15),
    dag=dag,
)

t2 = PythonOperator(
    task_id="clean_raw_csv",
    python_callable=data_cleaner,
    dag=dag,
)

t3 = MySqlOperator(
    task_id="create_mysql_table", 
    # reference connection to a database
    mysql_conn_id="mysql_conn",
    sql="create_table.sql",
    dag=dag,
)

t4 = MySqlOperator(
    task_id="insert_into_table", 
    # reference connection to a database
    mysql_conn_id="mysql_conn",
    sql="insert_into_table.sql",
    dag=dag,
)

t5 = MySqlOperator(
    task_id="select_from_table", 
    # reference connection to a database
    mysql_conn_id="mysql_conn",
    sql="select_from_table.sql",
    dag=dag,
)

t1 >> t2 >> t3 >> t4 >> t5
