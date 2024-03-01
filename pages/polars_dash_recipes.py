import dash
import dash_mantine_components as dmc

dash.register_page(__name__)


layout = [
    dmc.Title("Polars Dash Recipes", order=1),
    dmc.Text("This page contains some common code snippets for using Polars with Dash."),
    ]

