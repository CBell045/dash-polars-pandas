import dash
from dash import dcc, callback, Input, Output, State
import dash_mantine_components as dmc
import inspect
from queries import *

dash.register_page(__name__)


layout = [
    dmc.Title("Titanic", order=1),
    dmc.Text("We will compare the performance of Pandas and Polars on the class Titanic dataset."),
    dmc.Space(h=20),
    dmc.Grid(children=[
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Query 1 Pandas", order=5),
                show_code(query_1_pandas),
                dmc.Text(id="output-1-pandas")
            ]),
            # dmc.Card([
            #     dmc.Title("Query 2 Pandas", order=5),
            #     show_code(query_2_polars),
            #     # dmc.Text(id="output-1-pandas")
            # ]),
        ]),
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Query 1 Polars", order=5),
                show_code(query_1_polars),
                dmc.Text(id="output-1-polars")
            ])
        ]),
    ],
    gutter="xl",
    ),
    dmc.Button("Run Query 1", id="button-1"),
]


@callback(
    Output("output-1-pandas", "children"),
    Input("button-1", "n_clicks"),
)
def query_1(n_clicks):
    if n_clicks is None:
        return ""
    return timer(query_1_pandas)()
    