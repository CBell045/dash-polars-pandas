import dash
import dash_mantine_components as dmc
from dash import html

dash.register_page(__name__)

def code(string):
    return dmc.Prism(string, language="python")

def create_section(title, pandas_code, polars_code):
    return html.Div([
        dmc.Title(title, order=3, mt=20, mb=10),
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


layout = [
    dmc.Title("Polars Dash Recipes", order=1),
    dmc.Text("This cheat sheet outlines some common code snippets for using Polars with Dash."),
    dmc.Space(h=20),
    dmc.Divider(),

    # DF To Datatable
    create_section(
        "DF To Datatable",
        "df.to_dict('records')",
        "df.to_dicts() # Note: df.to_dict() will not work."
    ),

    # Unique Column Values
    create_section(
        "Get Unique Column Values",
        "df.country.unique()",
        "df.get_column('country').unique().to_list()"
    ),

    # Filtering
    create_section(
        "Filtering",
        "df[df['country'] == 'USA']",
        "df.filter(pl.col('country') == 'USA')"
    ),

    # Group By
    create_section(
        "Group By",
        "df.groupby('year').agg({'pop':'mean'})",
        "df.group_by('year').agg(pl.col('pop').mean())"
    ),

    # Sort
    create_section(
        "Sort",
        "df.sort_values('year')",
        "df.sort('year')"
    ),



    dmc.Space(h=20),
    dmc.Text("This page is a work in progress. Do you know of other semantic differences that were hard to convert to Polars? "),
    dmc.Anchor("Let me know!", href="mailto:chadbell045@gmail.com"),

]

