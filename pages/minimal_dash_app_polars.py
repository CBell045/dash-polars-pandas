import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
# import pandas as pd
import polars as pl
import dash_mantine_components as dmc
import inspect

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
df = pl.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# Get the code from minimal_dash_app_polars_code.py
file_name = "minimal_dash_app_polars_code.py"
with open(file_name, "r") as file:
    source_code = file.read()

# Register page
dash.register_page(__name__, path='/')

layout = html.Div([
    dmc.Title("Minimal Dash App in Polars", order=1),
    dmc.Text(["This example is from the ", dmc.Anchor("Dash documentation", href="https://dash.plotly.com/basic-callbacks"), ", rewritten with Polars instead of Pandas."]),
    dmc.Space(h=20),
    dmc.Divider(),

    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(
        # df.country.unique(), 
        df.get_column('country').unique().to_list(), 
        'Canada', 
        id='dropdown-selection'),

    dcc.Graph(id='graph-content'),

    # Show the code
    dmc.Space(h=30),
    dmc.Card([
        dmc.Prism(
            source_code,
            language="python"
        ),
    ]),
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df.filter(pl.col('country') == value)
    # dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')
