from dash import Dash, html, dash_table, dcc, html, callback, Output, Input
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

import datetime
from datetime import datetime as dt
import pathlib

# CSS Style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialise the app
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Archus Insights Dashboard Demo"

server = app.server
app.config.suppress_callback_exceptions = True

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

# Read data
df = pd.read_csv(DATA_PATH.joinpath("altered_healthcare_data.csv"))

def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description",
        children=[
            html.H5("Clinical Analytics"),
            html.H3("Welcome to the Clinical Analytics Dashboard"),
            html.Div(
                id="intro",
                children="Explore clinic patient volume by time of day, waiting time, and care score. Click on the heatmap to visualize patient experience at different time points.",
            ),
        ],
    )

app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("Archus.png"))],
        ),
    dcc.Tabs([
        dcc.Tab(label='HES Data', children=[
            dcc.Dropdown(options=[{'label': code, 'value': code} for code in df['PROCODE3'].unique()],
            id='provider', placeholder='Select a Trust'),
            dcc.Graph(figure={}, id='output_provider')
        ]),
        dcc.Tab(label='User Input', children=[
            html.Label('Enter text:'),
            dcc.Input(id='input-text', type='text', value=''),
        ]),
        dcc.Tab(label='Dropdown', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': 'Montréal'},
                    ]
                }
            )
        ]),
    ])
])

@app.callback(
    Output('output_provider', 'figure'),
    [Input('provider', 'value')]
)
def update_graph(provider):
    df_provider = df[(df['EPISTART'] >= '2021-04-01') & (df['PROCODE3'] == str(provider))]
    df_provider_count = df_provider.groupby('EPISTART').size().reset_index(name='count')
    fig = px.line(df_provider_count, x='EPISTART', y='count', title=f'Provider: {provider} Counts Over Time')
    # Update the y-axis label
    fig.update_layout(yaxis_title='Date')
    return fig

if __name__ == '__main__':
    app.run(debug=True)