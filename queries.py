import time
import pandas as pd
import polars as pl
import inspect
import dash_mantine_components as dmc

def show_code(function):
    # Get the full source code of the function
    full_source = inspect.getsource(function)

    # Split the source code into lines
    source_lines = full_source.split('\n')

    # Remove the first 4 spaces from each line
    source_lines = [line[4:] for line in source_lines]

    # Exclude the first and last line which contain def and the return statement
    body_lines = source_lines[1:-2]

    # Join the lines back together
    body_source = '\n'.join(body_lines)

    return dmc.Prism(
        body_source,
        language="python",
        trim=False,
    )

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        return end - start
    return wrapper


# Query 1
def query_1_pandas():
    df = pd.read_csv("data/titanic.csv")
    return df

def query_1_polars():
    df = pl.read_csv("data/titanic.csv")
    return df


# Query 2
titanic = pd.read_csv("data/titanic.csv")
def query_2_pandas():
    titanic["Age"]
    titanic["Age"].shape
    titanic[["Age", "Sex"]]
    titanic[titanic["Age"] > 35]
    titanic[(titanic["Pclass"] == 2) | (titanic["Pclass"] == 3)]
    titanic[titanic["Age"].notna()]
    titanic.loc[titanic["Age"] > 35, "Name"]
    return 

titanic_pl = pl.read_csv("data/titanic.csv")
def query_2_polars():
    titanic_pl.select("Age")
    titanic_pl.select("Age").shape
    titanic_pl.select(["Age", "Sex"])
    titanic_pl.filter(pl.col("Age") > 35)
    titanic_pl.filter(pl.col("Pclass").is_in([2, 3]))
    titanic_pl.filter(pl.col("Age").is_not_null())
    titanic_pl.filter(pl.col("Age") > 35).select(pl.col("Name"))
    return 

# Query 3
def query_3_pandas():
    df = pd.read_parquet('data/tpch/lineitem')
    return df

def query_3_polars():
    df = pl.read_parquet('data/tpch/lineitem/*')
    return df


# Query 4
lineitem_pd = pd.read_parquet('data/tpch/lineitem')
def query_4_pandas():
  (
    lineitem_pd[lineitem_pd['l_shipdate'].dt.date <= pd.to_datetime('1998-12-01').date() - pd.Timedelta(days=90)]
    .groupby(['l_returnflag', 'l_linestatus']).agg(
        sum_qty=pd.NamedAgg(column='l_quantity', aggfunc='sum'),
        sum_base_price=pd.NamedAgg(column='l_extendedprice', aggfunc='sum'),
        sum_disc_price=pd.NamedAgg(column='l_extendedprice', aggfunc=lambda x: (x * (1 - lineitem_pd['l_discount'])).sum()),
        sum_charge=pd.NamedAgg(column='l_extendedprice', aggfunc=lambda x: (x * (1 - lineitem_pd['l_discount'] * (1 + lineitem_pd['l_tax']))).sum()),
        avg_qty=pd.NamedAgg(column='l_quantity', aggfunc='mean'),
        avg_price=pd.NamedAgg(column='l_extendedprice', aggfunc='mean'),
        avg_disc=pd.NamedAgg(column='l_discount', aggfunc='mean'),
        count_order=pd.NamedAgg(column='l_orderkey', aggfunc='count')
    )
    .sort_values(['l_returnflag', 'l_linestatus'])
  )
  return


lineitem_pl = pl.read_parquet('data/tpch/lineitem/*')
def query_4_polars():
  (
    lineitem_pl.filter(pl.col('l_shipdate') <= pl.date(1998, 12, 1) - pl.duration(days=90))
    .group_by(['l_returnflag', 'l_linestatus']).agg(
        sum_qty=pl.col('l_quantity').sum(),
        sum_base_price=pl.col('l_extendedprice').sum(),
        sum_disc_price=(pl.col('l_extendedprice') * (1 - pl.col('l_discount'))).sum(),
        sum_charge=(pl.col('l_extendedprice') * (1 - pl.col('l_discount') * (1 + pl.col('l_tax')))).sum(),
        avg_qty=pl.col('l_quantity').mean(),
        avg_price=pl.col('l_extendedprice').mean(),
        avg_disc=pl.col('l_discount').mean(),
        count_order=pl.col('l_orderkey').count()
    )
    .sort(['l_returnflag', 'l_linestatus'])
  )
  return
