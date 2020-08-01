from airflow import DAG

from airflow.operators.dummy_operator import DummyOperator
from airflow.utils import timezone

default_args = {
    'owner': 'ODDS',
}
dag = DAG('dummy_pipeline',
            schedule_interval='*/5 * * * *',
            default_args=default_args,
            start_date=timezone.datetime(2020, 8, 1),
            catchup=False)

t1 = DummyOperator(task_id='my_dummy_task_1', dag=dag)
t2 = DummyOperator(task_id='my_dummy_task_2', dag=dag)
t3 = DummyOperator(task_id='my_dummy_task_3', dag=dag)
t4 = DummyOperator(task_id='my_dummy_task_4', dag=dag)
t5 = DummyOperator(task_id='my_dummy_task_5', dag=dag)
t6 = DummyOperator(task_id='my_dummy_task_6', dag=dag)
t7 = DummyOperator(task_id='my_dummy_task_7', dag=dag)
t8 = DummyOperator(task_id='my_dummy_task_8', dag=dag)


t1 >> t2 >> t3 >> t8
t1 >> t4 >> [t5, t6] >> t7 >> t8