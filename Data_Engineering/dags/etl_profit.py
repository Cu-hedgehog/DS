import datetime as dt
import pandas as pd
from tqdm import tqdm
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task
from pathlib import Path
from datetime import date, timedelta
import os

default_args = {'owner': 'admin',
                'start_date': dt.datetime(2021, 1, 20),
                }

@task(task_id="t1_extract", execution_timeout=timedelta(minutes=5), retries=5)
def extract(csv_path: Path = Path('/root/airflow/dags/data/profit_table.csv')) -> pd.DataFrame:
    """Функция для чтения данных из файла по указанному пути

    Args:
        csv_path (Path, optional): путь к файлу для чтения. 
        Значение по умолчанию ('/root/airflow/dags/data/profit_table.csv').

    Returns:
        pd.DataFrame: полученный после прочтения DataFrame
    """
    df = pd.read_csv(csv_path)
    print(df.head())
    return df
    
@task(task_id="t2_transform", execution_timeout=timedelta(minutes=5), retries=5)
def transform(profit_table: pd.DataFrame, current_date: date) -> pd.DataFrame:
    """ Собирает таблицу флагов активности по продуктам
        на основании прибыли и количеству совершёных транзакций
        
        :param profit_table: таблица с суммой и кол-вом транзакций
        :param current_date: дата расчёта флагов активности
        
        :return df_tmp: pandas-датафрейм флагов за указанную дату
    """
    current_date = pd.to_datetime(current_date)
    start_date = current_date - pd.DateOffset(months=2)
    end_date = current_date + pd.DateOffset(months=1)
    
    date_list = pd.date_range(
        start=start_date, end=end_date, freq='M'
    ).strftime('%Y-%m-01')
    
    df_tmp = (
        profit_table[profit_table['date'].isin(date_list)]
        .drop('date', axis=1)
        .groupby('id')
        .sum()
    )
    
    product_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for product in tqdm(product_list):
        df_tmp[f'flag_{product}'] = (
            df_tmp.apply(
                lambda x: x[f'sum_{product}'] != 0 and x[f'count_{product}'] != 0,
                axis=1
            ).astype(int)
        )
        
    df_tmp = df_tmp.filter(regex='flag').reset_index()
    
    return df_tmp

@task(task_id="t3_load", execution_timeout=timedelta(minutes=5))
def load(profit_table: pd.DataFrame, csv_target: Path = Path("/root/airflow/dags/data/activity_table.csv")) -> None:
    """Функция для сохранения полученной таблицы без перезаписи данных

    Args:
        profit_table (pd.DataFrame): преобразованный DataFrame, который необходимо сохранить 
        csv_target (Path, optional): путь для сохранения файла. 
        Значение по умолчанию ("/root/airflow/dags/data/activity_table.csv").
    """
    if not os.path.isdir(csv_target):
        profit_table.to_csv(csv_target, index=False)
    else:
        profit_table.to_csv(csv_target, mode='a', header=False, index=False)

@dag(dag_id='Almaeva_Elena_dag', schedule='0 0 5 * *', catchup=False, default_args = default_args)
def etl_base():
    t1_extract = extract()
    t2_transform = transform(t1_extract, date.today())
    t3_load = load(t2_transform)

    t1_extract >> t2_transform >> t3_load


dag_etl = etl_base()


if __name__ == "__main__":
    dag_etl.test()