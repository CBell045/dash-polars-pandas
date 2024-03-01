import dash
from dash import dcc, callback, Input, Output, State
import dash_mantine_components as dmc
import inspect
from queries import *
import plotly.express as px
import plotly.graph_objects as go
from dash_iconify import DashIconify

dash.register_page(__name__, path='/')

example_fig = go.Figure(layout=dict(height=250))


layout = [
    dmc.Title("Speed Comparison", order=1),
    dmc.Group([
        dmc.Text("This page allows you to visualize the performance difference between Polars and Pandas."),
        dmc.HoverCard(
                shadow="md",
                openDelay=1,
                closeDelay=1,
                children=[
                    dmc.HoverCardTarget(DashIconify(icon="feather:info", width=17)),
                    dmc.HoverCardDropdown(dmc.Alert("For simplicity in comparing to Pandas, these examples do not use LazyFrames. This is not a real benchmark and further optimizations could be implemented with Polars.", title="Disclaimer", color="red")),
                ],
            ),
        ]),
    dmc.Space(h=20),
    dmc.Divider(),
    dmc.Space(h=20),
    dmc.Title("Query 1: Read Titanic CSV", order=3),
    dmc.Text("We will start by reading in a familiar dataset — the Titanic."),
    dmc.Space(h=20),
    dmc.Grid(children=[
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Pandas", order=5),
                show_code(query_1_pandas),
            ], withBorder=True, shadow="md"),
        ]),
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Polars", order=5),
                show_code(query_1_polars),
            ], withBorder=True, shadow="md"),
        ]),
        dmc.Col(span=12, children=[
            dmc.Card([
                dmc.Button("Run Query 1", id="button-1"),
                dcc.Graph(figure=example_fig, id="output-1-fig"),
            ], withBorder=True, shadow="md"),
            
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
    