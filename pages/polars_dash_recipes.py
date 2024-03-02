import dash
import dash_mantine_components as dmc

dash.register_page(__name__)

def code(string):
    return dmc.Prism(string, language="python")

layout = [
    dmc.Title("Polars Dash Recipes", order=1),
    dmc.Text("This page contains some common code snippets for using Polars with Dash."),
    dmc.Space(h=20),
    dmc.Divider(),
    # Unique Column Values
    dmc.Space(h=20),
    dmc.Title("Get Unique Column Values", order=3),
    dmc.Space(h=10),
    dmc.Grid(children=[
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Pandas", order=5),
                code("""df.country.unique() """),
            ], withBorder=True, shadow="md"),
        ]),
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Polars", order=5),
                code("""df.get_column('country').unique().to_list() """),
            ], withBorder=True, shadow="md"),
        ]),
    ]),
    dmc.Space(h=20),
    # Filtering
    dmc.Space(h=20),
    dmc.Title("DF To Datatable", order=3),
    dmc.Space(h=10),
    dmc.Grid(children=[
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Pandas", order=5),
                code("""df.to_dict('records')"""),
            ], withBorder=True, shadow="md"),
        ]),
        dmc.Col(span=6, children=[
            dmc.Card([
                dmc.Title("Polars", order=5),
                code("""df.to_dicts() # Note: df.to_dict() will not work."""),
            ], withBorder=True, shadow="md"),
        ]),
    ]),
    dmc.Space(h=20),

    dmc.Space(h=20),
    dmc.Text("This page is a work in progress. Do you know of other semantic differences that were hard to convert to Polars? "),
    dmc.Anchor("Let me know!", href="mailto:chadbell045@gmail.com"),

]

