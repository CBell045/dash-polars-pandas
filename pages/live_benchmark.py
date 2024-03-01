import dash
from dash import dcc, callback, Input, Output, State
import dash_mantine_components as dmc
import inspect
from queries import *
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__)

example_fig = go.Figure(layout=dict(height=250))


layout = [
    dmc.Title("Live Benchmark", order=1),
    dmc.Text("This page allows you to visualize the performance difference between Polars and Pandas."),
    dmc.Space(h=20),
    dmc.Divider(),
    dmc.Space(h=20),
    dmc.Title("Titanic Query 1", order=3),
    dmc.Text("We will start by reading in a familiar dataset — the Titanic."),
    dmc.Space(h=20),
    dmc.Grid(children=[
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Pandas", order=5),
                show_code(query_1_pandas),
            ]),
        ]),
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Polars", order=5),
                show_code(query_1_polars),
            ]),
        ]),
        dmc.Col(span=12, children=[
            dmc.Card([
                dmc.Button("Run Query 1", id="button-1"),
                dcc.Graph(figure=example_fig, id="output-1-fig"),
            ]),
            
        ]),
    ],
    gutter="xl",
    ),
]


@callback(
    Output("output-1-fig", "figure"),
    Input("button-1", "n_clicks"),
)
def query_1(n_clicks):
    pandas_time = timer(query_1_pandas)()
    polars_time = timer(query_1_polars)()
    fig = px.bar(y=["Polars", "Pandas"], x=[polars_time, pandas_time], template='none', height=250)
    return fig
    