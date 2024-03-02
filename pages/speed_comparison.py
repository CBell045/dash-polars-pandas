import dash
from dash import dcc, callback, Input, Output, State, html, MATCH
import dash_mantine_components as dmc
from queries import *
import plotly.express as px
import plotly.graph_objects as go
from dash_iconify import DashIconify

# Initialize the page
dash.register_page(__name__, path='/')

# Create a query from the query number, title, and text
def create_query(q_number, title, text):
    return html.Div([
        dmc.Space(h=20),
        dmc.Title(f"Query {q_number}: {title}", order=3),
        dmc.Text(text),
        dmc.Space(h=20),
        dmc.Grid(children=[
            dmc.Col(span=6, children=[
                dmc.Card([
                    dmc.Title("Pandas", order=5),
                    show_code(globals()[f"query_{q_number}_pandas"]),
                    
                ], withBorder=True, shadow="md"),
            ]),
            dmc.Col(span=6, children=[
                dmc.Card([
                    dmc.Title("Polars", order=5),
                    show_code(globals()[f"query_{q_number}_polars"]),
                ], withBorder=True, shadow="md"),
            ]),
            dmc.Col(span=12, children=[
                dmc.Card([
                    dmc.Group([
                        dmc.Button(f"Run Query {q_number}", id={"type": "button", "index": q_number}),
                        dmc.Text(children="Pandas vs Polars Time: ", size='sm'),
                        dmc.Text(size='sm', id={"type": "time", "index": q_number}),
                    ]),
                    
                    dcc.Graph(figure=go.Figure(layout=dict(height=250)), id={"type": "fig", "index": q_number}),

                ], withBorder=True, shadow="md"),
                
            ]),
        ],
        gutter="xl",
        )
    ])


# Define the layout
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
    create_query(1, "Read Titanic CSV", "We will start by reading in a familiar dataset — the Titanic."),
    create_query(3, "Read TCP-H Parquet", "Ramping up -- we will read in a larger dataset, the TCP-H benchmark."),
]




# Pattern matching callback to find which button was clicked and run the corresponding queries
@callback(
    Output({"type": "fig", "index": MATCH}, "figure"),
    Output({"type": "time", "index": MATCH}, "children"),
    Input({"type": "button", "index": MATCH}, "n_clicks"),
    State({"type": "button", "index": MATCH}, "id"),
)
def run_queries(n_clicks, id):
    # Get the query number from the id
    q_number = id.get("index")

    # Get the function names from the query number
    pandas_func = globals()[f"query_{q_number}_pandas"]
    polars_func = globals()[f"query_{q_number}_polars"]

    # Get the time it takes to run the functions
    pandas_time = timer(pandas_func)()
    polars_time = timer(polars_func)()

    # Create the figure
    fig = px.bar(y=["Polars", "Pandas"], x=[polars_time, pandas_time], template='none', height=250)

    # Return the figure and the time it took to run the functions
    return fig, f"{pandas_time:.4f}s vs {polars_time:.4f}s"
    