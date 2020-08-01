from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils import timezone

import pandas

default_args = {
    'owner': 'ODDS',
}
dag = DAG('product_price_pipeline',
            default_args=default_args,
            start_date=timezone.datetime(2020, 8, 1),
            catchup=False)

def get_product_upc_and_description():
    df = pandas.read_csv('products-lookup-table.csv', header=1)
    new_df = df[['UPC', 'DESCRIPTION']]
    new_df.to_csv('product_upc_and_description.csv', index=False)

def get_transaction_upc_and_price():
    df = pandas.read_csv('transaction-table.csv', header=1)
    new_df = df[['UPC', 'PRICE']]
    new_df.to_csv('transaction_upc_and_price.csv', index=False)

def merge():
    df_product_description = pandas.read_csv('product_upc_and_description.csv')
    df_product_price = pandas.read_csv('transaction_upc_and_price.csv')
    new_df = pandas.merge(df_product_description, df_product_price, left_on='UPC', right_on='UPC')
    # new_df = df_product_description.join(df_product_price, on='UPC', how='left')
    new_df.to_csv('product_and_price.csv', index=False)

start = DummyOperator(
                task_id='start', 
                dag=dag
)

get_product_upc_and_description = PythonOperator(
                task_id='get_product_upc_and_description',
                python_callable=get_product_upc_and_description,
                dag=dag
)

get_transaction_upc_and_price = PythonOperator(
                task_id='get_transaction_upc_and_price',
                python_callable=get_transaction_upc_and_price,
                dag=dag
)

merge = PythonOperator(
                task_id='merge',
                python_callable=merge,
                dag=dag
)

end = DummyOperator(task_id='end', 
                dag=dag
)


start >> [get_product_upc_and_description, get_transaction_upc_and_price] >> merge >> end