# -*- coding: utf-8 -*-
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import pandas as pd
import plotly.graph_objs as gobs
import requests

# TODO Move the Dash css to local directory to edit
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']

external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']


server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts, server=server)


# DATA IMPORT
# ============
countries = requests.get('https://api.covid19api.com/countries').json()
country_slugs = sorted([country['Slug'] for country in countries])

base = 'https://api.covid19api.com/dayone/country/'

indicators = ['confirmed', 'deaths']

countries_data = []


for country_slug in country_slugs:
    print('Retrieving data for Country {}'.format(country_slug))
    for indicator in indicators:
        url = base + country_slug + '/status/' + indicator
        country_data = requests.get(url).json()

        country_df = pd.DataFrame(country_data)

        countries_data.append(country_df)
    
data = pd.concat(countries_data)
data['Date'] = pd.to_datetime(data['Date'])


# Group the data by Country, Status (indicator) and Date to aggregate the regional data
data = data.groupby(['Country', 'Status', 'Date']).sum().reset_index()
data.sort_values(['Country', 'Status', 'Date'], inplace=True)

country_names = data['Country'].unique().tolist()
indicator_names = data['Status'].unique().tolist()

# CONTROLLER
# ===========

country_selector = dcc.Dropdown(
    id='country-selector',
    options=[{'label': i, 'value': i} for i in data["Country"].unique()],
    value=country_names,
    multi=True
)

indicator_selector = dcc.Dropdown(
    id='indicator-selector',
    options=[{'label': i, 'value': i} for i in data["Status"].unique()],
    value='confirmed',
    multi=False
)

# PLOT
# ====

plot = html.Div(id="plot-container",
                children=[dcc.Graph(id="main-plot")])

# STRUCTURE
# =========

header = html.Div([
    html.H1("COVID-19 Time Series")
])

app.layout = html.Div([
    header,
    dcc.Loading(plot),
    country_selector,
    indicator_selector
])


# CHART UPDATING
# ==============

@app.callback(
    dash.dependencies.Output('main-plot', 'figure'),
    [
        dash.dependencies.Input('country-selector', 'value'),
        dash.dependencies.Input('indicator-selector', 'value')
    ]
)
def create_graph(country, indicator):

    df = data[data["Status"] == indicator]

    if isinstance(country, str):
        df = df[df["Country"] == country]
    else:
        df = df[df["Country"].isin(country)]

    traces = []
    for country in df["Country"].unique():
        _data = df[df["Country"] == country]
        traces.append(gobs.Scatter(
            x=_data['Date'],
            y=_data['Cases'],
            name=country
        ))

    return {
        'data': traces,
        'layout': gobs.Layout(
            xaxis={"title": "Date"},
            yaxis={"title": indicator},
            height=625,
            showlegend=True,
            hovermode="closest"
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)