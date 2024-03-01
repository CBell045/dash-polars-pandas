import dash
import dash_mantine_components as dmc

dash.register_page(__name__)


layout = [
    dmc.Title("Polars Dash Recipes", order=1),
    dmc.Text("This page contains some common code snippets for using Polars with Dash."),
    dmc.Space(h=20),
    dmc.Divider(),
    dmc.Space(h=20),
    dmc.Title("How To Get Unique Column Values", order=3),
    dmc.Space(h=10),
    dmc.Grid(children=[
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Pandas", order=5),
                dmc.Prism(
                    """df.country.unique() """, language="python"),
            ], withBorder=True, shadow="md"),
        ]),
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Polars", order=5),
                dmc.Prism("""df.get_column('country').unique().to_list() """, language="python"),
            ], withBorder=True, shadow="md"),
        ]),
    ]),
]

