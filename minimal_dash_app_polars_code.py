from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
# import pandas as pd
import polars as pl

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
df = pl.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(
        # df.country.unique(), 
        df.get_column('country').unique().to_list(),
        'Canada', 
        id='dropdown-selection'
        ),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    # dff = df[df.country==value]
    dff = df.filter(pl.col('country') == value)
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)
