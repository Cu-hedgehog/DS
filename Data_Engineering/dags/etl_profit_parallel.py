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
    
@task(task_id="t2_pre_transform", execution_timeout=timedelta(minutes=5), retries=5)
def pre_transform(profit_table: pd.DataFrame, current_date: date) -> pd.DataFrame:
    """Данная функция преобрабатывает DataFrame, выбирая необходимые даты из таблицы

    Args:
        profit_table (pd.DataFrame): таблица с суммой и кол-вом транзакций
        current_date (date): дата расчёта флагов активности

    Returns:
        pd.DataFrame: преобработанный DataFrame
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
    
    return df_tmp

@task(task_id="t3_transform", retries=5)
def transform(profit_table: pd.DataFrame, product_id: str) -> pd.DataFrame:
    """Данная функция предназначена для обработки отдельного столбца по продукту

    Args:
        profit_table (pd.DataFrame): предобработанная таблица с суммой и кол-вом транзакций
        product_id (str): id продукта для которого расставляются флаги активности

    Returns:
        pd.DataFrame: DataFrame флагов за указанную дату на указанный продукт
    """
    tmp_table = profit_table.copy()
    column_name = 'flag_' + product_id
    tmp_table[column_name] = tmp_table.apply(
        func=lambda row: row["sum_" + product_id] != 0 and row["count_" + product_id] != 0,
        axis=1,
    ).astype(int)

    return tmp_table.filter(regex='flag').reset_index()

@task(task_id="t4_load", execution_timeout=timedelta(minutes=5))
def load(tables_list: tuple[pd.DataFrame, ...], csv_target: Path = Path("/root/airflow/dags/data/activity_table.csv")) -> None:
    """Данная функция объединяет полученные столбцы с флагами по каждому продукты
    и сохраняет в конечный файл не перезаписывая его

    Args:
        tables_list (tuple[pd.DataFrame, ...]): список датафреймов с флагами по каждому продукту
        csv_target (Path, optional): путь для сохранения итого файла. 
        Значение по умолчанию("/root/airflow/dags/data/activity_table.csv").
    """
    for i in range(len(tables_list)):
        if i == 0: merged_df = tables_list[i]
        else: merged_df = pd.merge(merged_df, tables_list[i], on="id", how="outer")

    if not os.path.isdir(csv_target):
        merged_df.to_csv(csv_target, index=False)
    else:
        merged_df.to_csv(csv_target, mode='a', header=False, index=False)

@dag(dag_id='Almaeva_Elena_parallel_dag', schedule='0 0 5 * *', catchup=False, default_args = default_args)
def etl_parallel():

    t1_extract = extract()
    t2_pre_transform = pre_transform(t1_extract, date.today())

    t3_transform = tuple(
        transform.override(task_id=f"product_{i}")(
            profit_table=t2_pre_transform,
            product_id=i,
        )
        for i in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
    )
    
    t4_load = load(t3_transform)

    t1_extract >> t2_pre_transform >> t3_transform >> t4_load


dag_etl = etl_parallel()


if __name__ == "__main__":
    dag_etl.test()