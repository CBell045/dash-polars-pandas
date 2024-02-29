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

    # Exclude the first and last line which contain def and the return statement
    body_lines = source_lines[1:-2]  

    # Join the lines back together
    body_source = '\n'.join(body_lines)
    
    return dmc.Prism(
        body_source,
        language="python"
    )

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        return f"{func.__name__} took {end - start} seconds"
    return wrapper


# Query 1
def query_1_pandas():
    df = pd.read_csv("data/titanic.csv")
    return df

def query_1_polars():
    df = pl.read_csv("data/titanic.csv")
    return df

df = pl.read_csv("data/titanic.csv")
def query_2_polars():
    df = (
        df.filter(pl.col('l_shipdate') <= pl.date(1998, 12, 1) - pl.duration(days=90))
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
    return df