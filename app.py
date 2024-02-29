import dash
import dash_mantine_components as dmc
from dash import html, Dash, dcc, Input, Output, State


# Initialize Dash app.
app = Dash(__name__, use_pages=True, title="Dash: Polars vs Pandas", suppress_callback_exceptions=True)


nav_items = {
    page['name'].replace("-", " ").title(): page['path'] for page in dash.page_registry.values()
}

def serve_layout(): 
    return html.Div([
        dcc.Location(id="url"),
        dmc.MantineProvider(
            id='app', 
            withGlobalStyles=True,
            theme={"primaryColor": "blue",
                "fontFamily": "'Inter', sans-serif",
                    "components": {
                        "Title": {
                            "styles": {
                                "root": {
                                    "font-family": "Inter", 
                                    "fontWeight": 600, 
                                        }
                                    }
                                }
                            }
                        },
            children=dmc.Grid(
                grow=True,
                children=[
                    dmc.Col(
                        span=1,
                        p=0,
                        children=[
                            dmc.Navbar(
                                p="md",
                                children=[
                                    dmc.Space(h=30),
                                    # Title
                                    dmc.Center([
                                        dmc.Title("Dash Polars vs Pandas", order=5),
                                    ]),
                                    dmc.Space(h=20),
                                    *[dmc.NavLink(
                                        label=page,
                                        href=path,
                                        id=page,
                                    ) for page, path in nav_items.items()],
                                ],
                            )],
                    ),
                    dmc.Col(
                        span=8,
                        p="xl",
                        style={'background-color': '#f1f5f9'},
                        children=[
                            dmc.Container([
                                dmc.Space(h=30),
                                dash.page_container,
                            ]),
                        ],
                    ),
                ],
            )
        )
    ])

app.layout = serve_layout


""" Set active navlink """
page_outputs = [Output(label, "active") for label in nav_items.keys()]
@app.callback(
    *page_outputs,
    Input("url", "pathname"),
)
def set_active_navlink(pathname):
    return [pathname == href for href in nav_items.values()]


if __name__ == "__main__":
    app.run_server(debug=True)