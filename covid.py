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
docs = []

# dirs = ['biorxiv_medrxiv',"comm_use_subset", "noncomm_use_subset", "custom_license"]
dirs = ['biorxiv_medrxiv']
for d in dirs: 
    print(d)
    for file in tqdm(os.listdir(f"{d}/{d}")):
        file_path = f"{d}/{d}/{file}"
        j = json.load(open(file_path, "rb"))

        title = j["metadata"]["title"]

        try:
            abstract = j['abstract'][0]

        except:
            abtract = ""

        full_text = ""

        for text in j['body_text']:

            full_text += text['text']+'\n\n'

        
        docs.append([title, abstract, full_text])

df  = pd.DataFrame(docs, columns=['title', 'abstract', 'full_text'])
# print(df.head())

# figuring out incubation period of the virus
incubation = df[df['full_text'].str.contains('incubation')]
# print(incubation.head())

paras = incubation['full_text'].values
incubation_time = []

for text in paras:
    for sentence in text.split(". "):
        if "incubation" in sentence:
            day = re.findall(r" \d{1,2} day", sentence)
            if len(day) == 1:
                num = day[0].split(" ")
                incubation_time.append(float(num[1]))


print(incubation_time)

# PLOT
# ====

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Wash your hands, stay safe   ',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='COVID 19: Displaying incubation periods.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': incubation_time, 'y': list(np.arange(1,len(incubation_time))), 'type': 'bar'},
                
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])


# CHART UPDATING
# ==============



if __name__ == '__main__':
    app.run_server(debug=True)