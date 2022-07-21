from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
# from globals import *
from app import *

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from dash.exceptions import PreventUpdate

card_style_icon = {
    'color': '#fff',
    'textAlign': 'center',
    'fontSize': '2.5rem',
    'margin': 'auto',
}

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        # Banca Atual
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Saldo Banca Atual'),
                    html.H5('R$ 1.287,22', id='current_balance', style={}),
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-university', style=card_style_icon),
                    color='warning',
                    style={'max-width': 75, 'height': 100, 'margin-left': '-10px', 'margin-right': '10px'}
                ),
            ]),
        ], width=4),

        # Green
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Total Greens'),
                    html.H5('R$ 759,22', id='green_balance', style={}),
                ], style={'padding-left': '25px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-smile-o', style=card_style_icon),
                    color='success',
                    style={'max-width': 75, 'height': 100, 'margin-left': '-10px', 'margin-right': '10px'}
                ),
            ]),
        ], width=4),

        # Red
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Total Reds'),
                    html.H5('-R$ 366,28', id='red_balance', style={}),
                ], style={'padding-left': '25px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-frown-o', style=card_style_icon),
                    color='danger',
                    style={'max-width': 75, 'height': 100, 'margin-left': '-10px', 'margin-right': '10px'}
                ),
            ]),
        ], width=4),
    ], style={'margin': '10px'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Filtrar Entradas', className='card-header'),
                html.Label('Entradas Greens', style={'margin-top': '10px'}),
                html.Div(
                    dcc.Dropdown(
                        id='dropdown-greens',
                        clearable=False,
                        style={'width': '100%'},
                        persistence=True,
                        persistence_type='session',
                        multi=True)
                ),
                html.Label('Entradas Reds', style={'margin-top': '10px'}),
                html.Div(
                    dcc.Dropdown(
                        id='dropdown-reds',
                        clearable=False,
                        style={'width': '100%'},
                        persistence=True,
                        persistence_type='session',
                        multi=True)
                ),

                html.Legend('Período de Análise', style={'margin-top': '10px'}),
                dcc.DatePickerRange(
                    id='picker-date-config',
                    month_format='Do MMM, YY',
                    end_date_placeholder_text='Data...',
                    start_date=datetime(2022, 4, 1).date(),
                    end_date=datetime.today() + timedelta(days=31),
                    updatemode='singledate',
                    style={'z-index': '100'}),
            ], style={'padding': '25px', 'height': '100%', 'margin-right': '10px'}),
        ], width=4),

        dbc.Col(
            dbc.Card(
                dcc.Graph(id='graph-entries'),
                style={'padding': '10px', 'height': '100%', 'margin-right': '10px'}), width=8
        ),
    ], style={'margin': '10px'}),

    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='graph-2'), style={'padding': '10px', 'margin': '10px'}), width=6),
        dbc.Col(dbc.Card(dcc.Graph(id='graph-2'), style={'padding': '10px', 'margin-right': '10px'}), width=3),
        dbc.Col(dbc.Card(dcc.Graph(id='graph-2'), style={'padding': '10px', 'margin-right': '20px'}), width=3),
    ]),

])

# =========  Callbacks  =========== #
