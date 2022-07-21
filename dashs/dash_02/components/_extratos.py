import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        html.Legend('Tabela de Entradas Red'),
        html.Div(id='table-entries-red', className='dbc'),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-entries-red', style={'margin-right': '20px'}),
        ], width=9),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Entradas Red'),
                    html.Legend("-R$ 366,28 ", id="value-entries-red", style={'font-size': '3rem'}),
                    html.H6('Total de Reds'),
                ], style={'text-align': 'center', 'padding-top': '30px'}),
            ], style={'margin-right': '20px'}),
        ], width=3),
    ]),
], style={'padding': '10px'})

# =========  Callbacks  =========== #
# Tabela
