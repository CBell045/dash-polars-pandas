import dash
import dash_mantine_components as dmc
from dash import html, dcc
import dash_ag_grid as dag
import polars as pl

dash.register_page(__name__)

def code(string):
    return dmc.Prism(string, language="python")

def create_section(title, text, pandas_code, polars_code):
    return html.Div([
        dmc.Title(title, order=3, mt=20),
        dmc.Text(text, mb=5),
        dmc.Grid(children=[
            dmc.Col(span=6, children=[
                dmc.Card([
                    dmc.Title("Pandas", order=5),
                    code(pandas_code),
                ], withBorder=True, shadow="md"),
            ]),
            dmc.Col(span=6, children=[
                dmc.Card([
                    dmc.Title("Polars", order=5),
                    code(polars_code),
                ], withBorder=True, shadow="md"),
            ]),
        ]),
        dmc.Space(h=20),
    ])

df = pl.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

layout = [
    dmc.Title("Polars Dash Recipes", order=1),
    dmc.Text("This cheat sheet outlines some common code snippets for using Polars with Dash."),
    dmc.Space(h=20),
    dmc.Divider(),

    # Import Libraries
    create_section(
        "Import Libraries",
        "To import the libraries:",
        "import pandas as pd",
        "import polars as pl"
    ),

    # Read CSV
    create_section(
        "Read CSV",
        "To read a CSV file into a DataFrame:",
        "pd.read_csv('data.csv')",
        "pl.read_csv('data.csv')",
),

    # Unique Column Values
    create_section(
        "Get Unique Column Values",
        "To get the unique values in a column (e.g. for a dropdown):",
        "df.country.unique()",
        "df.get_column('country').unique().to_list()"
    ),

    # Filtering
    create_section(
        "Filtering",
        "To filter a DataFrame:",
        """
        df[(df['year']==2007) & (df['country']=='Armenia')]
# or
df.query("year==2007 & country=='Armenia'")
        """,
        """
        df.filter(year=2007, country='Armenia')
# or
df.filter(pl.col('year')==2007, pl.col('country')=='Armenia')
        """
    ),

    # Group By
    create_section(
        "Group By",
        "To group by a column and aggregate:",
        "df.groupby('year').agg({'pop':'mean'})",
        "df.group_by('year').agg(pl.col('pop').mean())"
    ),

    # Sort
    create_section(
        "Sort",
        "To sort a DataFrame:",
        "df.sort_values('year')",
        "df.sort('year')"
    ),

    # Add Column
    create_section(
        "Add Column",
        "To add a column to a DataFrame:",
        "df['new_column'] = df['pop'] / 1_000_000",
        "df.with_columns((pl.col('pop') / 1_000_000).alias('new_column'))"
    ),

    # Select Columns
    create_section(
        "Select Columns",
        "To select columns from a DataFrame:",
        "df.loc[:, ['year', 'pop']]",
        "df.select('year', 'pop')"
    ),


    # Ploty Express
    create_section(
        "Plotly Express",
        "To create a Plotly Express chart from a DataFrame:",
        """
px.scatter(
  df.query("year==2007"), x="gdpPercap", y="lifeExp", 
  size="pop", color="continent", 
  hover_name="country", log_x=True, size_max=60
)
""",
        """
px.scatter(
  df.filter(pl.col('year')==2007), x="gdpPercap", y="lifeExp", 
  size="pop", color="continent",
  hover_name="country", log_x=True, size_max=60
)
"""
    ),

    # Dash Ag-Grid
    create_section(
        "DataFrame To Dash Ag-Grid",
        "To create a DataTable from a DataFrame:",
        """
dag.AgGrid(
  columnDefs=[{"field": c} for c in df.columns],  
  rowData=df.to_dict('records'),
),
""",
        """
dag.AgGrid(
  columnDefs=[{"field": c} for c in df.columns],  
  rowData=df.to_dicts(), # Note: df.to_dict() will not work.
),
        """
    ),


    dmc.Space(h=20),
    dmc.Text("This page is a work in progress. Do you know of other semantic differences that were hard to convert to Polars? "),
    dmc.Anchor("Let me know!", href="mailto:chadbell045@gmail.com"),

]

