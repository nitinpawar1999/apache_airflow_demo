import os
from airflow import DAG
from airflow.operators.python import PythonOperator

from airflow.utils.dates import days_ago

args = {
    'owner': 'manaswini',
}

dag = DAG(
    dag_id='demo_task',
    default_args=args,
    start_date=days_ago(1),
    schedule_interval=None
)


def create_a_file(**context):
    print(f"In the job, msg is this {context['dag_run'].conf['msg']}")
    try:
        with open('file_1.txt', mode="w") as f:
            f.write(context['dag_run'].conf['msg'])
        print('File created')
    except Exception as e:
        print(e)

def rename_a_file():
    path = ""
    os.rename(path+'file_1.txt', path+'file_2.txt')

def remove_a_file():
    if os.path.isfile('file_2.txt'):
        os.remove('file_1.txt')
        print("success")
    else:    
        print("File doesn't exists!")

create_a_file_op = PythonOperator(
    task_id='create_a_file',
    python_callable=create_a_file,
    dag=dag,
)

rename_a_file_op = PythonOperator(
    task_id='rename_a_file',
    python_callable=rename_a_file,
    dag=dag,
)

remove_a_file_op = PythonOperator(
    task_id='remove_a_file',
    python_callable=remove_a_file,
    dag=dag,   
)

create_a_file_op >> rename_a_file_op >> remove_a_file_op