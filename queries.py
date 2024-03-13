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
def query_2_pandas():
    titanic = pd.read_csv("data/titanic.csv")
    titanic["Age"]
    titanic["Age"].shape
    titanic[["Age", "Sex"]]
    titanic[titanic["Age"] > 35]
    titanic[(titanic["Pclass"] == 2) | (titanic["Pclass"] == 3)]
    titanic[titanic["Age"].notna()]
    titanic.loc[titanic["Age"] > 35, "Name"]
    return 

def query_2_polars():
    titanic = pl.read_csv("data/titanic.csv")
    titanic.select("Age")
    titanic.select("Age").shape
    titanic.select(["Age", "Sex"])
    titanic.filter(pl.col("Age") > 35)
    titanic.filter(pl.col("Pclass").is_in([2, 3]))
    titanic.filter(pl.col("Age").is_not_null())
    titanic.filter(pl.col("Age") > 35).select(pl.col("Name"))
    return 


# Query 3
def query_3_pandas():
    df = pd.read_parquet('data/tpch/lineitem')
    return df

def query_3_polars():
    df = pl.read_parquet('data/tpch/lineitem/*')
    return df


# Query 4
def query_4_pandas():
    df = pd.read_parquet('data/tpch/lineitem')
    (
     df[df['l_shipdate'].dt.date <= pd.to_datetime('1998-12-01').date() - pd.Timedelta(days=90)]
     .groupby(['l_returnflag', 'l_linestatus']).agg(
        sum_qty=pd.NamedAgg(column='l_quantity', aggfunc='sum'),
        sum_base_price=pd.NamedAgg(column='l_extendedprice', aggfunc='sum'),
        sum_disc_price=pd.NamedAgg(column='l_extendedprice', aggfunc=lambda x: (x * (1 - df['l_discount'])).sum()),
        sum_charge=pd.NamedAgg(column='l_extendedprice', aggfunc=lambda x: (x * (1 - df['l_discount'] * (1 + df['l_tax']))).sum()),
        avg_qty=pd.NamedAgg(column='l_quantity', aggfunc='mean'),
        avg_price=pd.NamedAgg(column='l_extendedprice', aggfunc='mean'),
        avg_disc=pd.NamedAgg(column='l_discount', aggfunc='mean'),
        count_order=pd.NamedAgg(column='l_orderkey', aggfunc='count')
     )
    .sort_values(['l_returnflag', 'l_linestatus'])
    )
    return


def query_4_polars():
    (
     pl.read_parquet('data/tpch/lineitem/*')
     .filter(pl.col('l_shipdate') <= pl.date(1998, 12, 1) - pl.duration(days=90))
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


# Query 5
def query_5_pandas():
    var_1 = 15
    var_2 = "BRASS"
    var_3 = "EUROPE"

    region_df = pd.read_parquet('data/tpch/region')
    nation_df = pd.read_parquet('data/tpch/nation')
    supplier_df = pd.read_parquet('data/tpch/supplier')
    part_df = pd.read_parquet('data/tpch/part')
    part_supp_df = pd.read_parquet('data/tpch/partsupp')

    result_q1 = (
        part_df.merge(part_supp_df, left_on="p_partkey", right_on="ps_partkey")
        .merge(supplier_df, left_on="ps_suppkey", right_on="s_suppkey")
        .merge(nation_df, left_on="s_nationkey", right_on="n_nationkey")
        .merge(region_df, left_on="n_regionkey", right_on="r_regionkey")
        .loc[lambda x: x['p_size'] == var_1]
        .loc[lambda x: x['p_type'].str.endswith(var_2)]
        .loc[lambda x: x['r_name'] == var_3]
    )

    final_cols = [
        "s_acctbal",
        "s_name",
        "n_name",
        "p_partkey",
        "p_mfgr",
        "s_address",
        "s_phone",
        "s_comment",
    ]

    q_final = (
        result_q1.groupby("p_partkey")
        .agg({'ps_supplycost': 'min'})
        .merge(result_q1, on=["p_partkey", "ps_supplycost"])
        [final_cols]
        .sort_values(
            by=["s_acctbal", "n_name", "s_name", "p_partkey"],
            ascending=[False, True, True, True],
        )
        .head(100)
    )

    return q_final


def query_5_polars():
    var_1 = 15
    var_2 = "BRASS"
    var_3 = "EUROPE"

    region_df = pl.scan_parquet('data/tpch/region/*')
    nation_df = pl.scan_parquet('data/tpch/nation/*')
    supplier_df = pl.scan_parquet('data/tpch/supplier/*')
    part_df = pl.scan_parquet('data/tpch/part/*')
    part_supp_df = pl.scan_parquet('data/tpch/partsupp/*')

    result_q1 = (
        part_df.join(part_supp_df, left_on="p_partkey", right_on="ps_partkey")
        .join(supplier_df, left_on="ps_suppkey", right_on="s_suppkey")
        .join(nation_df, left_on="s_nationkey", right_on="n_nationkey")
        .join(region_df, left_on="n_regionkey", right_on="r_regionkey")
        .filter(pl.col("p_size") == var_1)
        .filter(pl.col("p_type").str.ends_with(var_2))
        .filter(pl.col("r_name") == var_3)
    ).cache()

    final_cols = [
        "s_acctbal",
        "s_name",
        "n_name",
        "p_partkey",
        "p_mfgr",
        "s_address",
        "s_phone",
        "s_comment",
    ]

    q_final = (
        result_q1.group_by("p_partkey")
        .agg(pl.min("ps_supplycost"))
        .join(result_q1, on=["p_partkey", "ps_supplycost"])
        .select(final_cols)
        .sort(
            by=["s_acctbal", "n_name", "s_name", "p_partkey"],
            descending=[True, False, False, False],
        )
        .limit(100)
    )

    return q_final.collect()

