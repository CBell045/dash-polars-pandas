import dash
import dash_mantine_components as dmc
from dash import html, Dash, dcc, Input, Output, State
from dash_iconify import DashIconify
from collections import OrderedDict

# Initialize Dash app.
app = Dash(__name__, use_pages=True, title="Dash: Polars vs Pandas", suppress_callback_exceptions=True)

# Initialize the server
server = app.server

# Create the nav pages by removing underscores and capitalizing them
nav_items = {
    page['name'].replace("_", " ").title(): page['path'] for page in dash.page_registry.values()
}
nav_items = OrderedDict(sorted(nav_items.items(), key=lambda x: x[0].lower()))

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
                                },
                        "NavLink": {
                            "styles": {
                                "root": {
                                    "border-radius": 8,
                                        }
                                    }
                                },
                                
                            }
                        },
            children=[
                dmc.Grid(
                    # grow=True,
                    children=[
                        dmc.Col(
                            sm=12,
                            md=2,
                            p=0,
                            children=[
                                dmc.Navbar(
                                    p="md",
                                    withBorder=False,
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
                                )
                                
                                ],
                        ),
                        dmc.Col(
                            sm=12,
                            md=10,
                            style={'backgroundColor': '#f1f5f9'},
                            children=[
                                dmc.Container(children=[
                                    dmc.Space(h=30),
                                    dash.page_container, 
                                ],
                                p='xl',
                                fluid=True,
                                ),
                            ],
                        ),
                        dmc.Col(
                            span=12,
                                children=[
                                    dmc.Group(
                                        m="md",
                                        children=[
                                            "By Chad Bell",
                                            dmc.Anchor(
                                                href="https://www.linkedin.com/in/chadbell045/",
                                                children=DashIconify(icon="mdi:linkedin", width=28, color="black")
                                            ),
                                            dmc.Anchor(
                                                href="https://github.com/CBell045/dash-polars-pandas",
                                                children=DashIconify(icon="mdi:github", width=28, color="black")
                                            ),
                                            dmc.Anchor(
                                                href="mailto:chadbell045@gmail.com",
                                                children=DashIconify(icon="heroicons:envelope-16-solid", width=28, color="black")
                                            ),
                                                
                                        ],
                                            
                                    ),
                                            
                                ],
                            ),
                    ],
                ),
            ],
        )
    ])

# Dynamically serve the layout
app.layout = serve_layout



page_outputs = [Output(label, "active") for label in nav_items.keys()]
@app.callback(
    *page_outputs,
    Input("url", "pathname"),
)
def set_active_navlink(pathname):
    """ Set active navlinks """
    return [pathname == href for href in nav_items.values()]


if __name__ == "__main__":
    app.run_server(debug=True)