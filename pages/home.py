import dash
import dash_mantine_components as dmc

dash.register_page(__name__, path='/')


layout = [
    dmc.Title("Home", order=1),
    dmc.Text("Welcome to Dash: Polars vs Pandas!"),
    dmc.Space(h=20),
    dmc.Divider(),
    dmc.Space(h=20),
    dmc.Title("What?", order=2),
    dmc.Text("This app explores Polars and compares it to Pandas."),
    dmc.Title("Why?", order=2),
    dmc.Text("Polars is a significantly faster dataframe library than Pandas. Check out the Speed Comparison page to see the difference."),
    dmc.Title("How?", order=2),
    dmc.Text("It is fairly simple to make the switch from Pandas to Polars. Check out teh Minimal Dash App (in Polars) and the common Polars Dash Recipes. "),
    ]

