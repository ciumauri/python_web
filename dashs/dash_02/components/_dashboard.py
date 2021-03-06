import calendar
from datetime import date, datetime, timedelta

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# from globals import *
from app import *
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

card_style_icon = {
    'color': '#fff',
    'textAlign': 'center',
    'fontSize': '2.5rem',
    'margin': 'auto',
}

graph_margin = dict(t=25, b=0, l=25, r=25)

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        # Banca Atual
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Saldo Banca Atual'),
                    html.H5('R$ 1.285,22', id='current_balance', style={}),
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
                dbc.Card(
                    html.Div(className='fa fa-smile-o', style=card_style_icon),
                    color='success',
                    style={'max-width': 75, 'height': 100, 'margin-left': '1px'}
                ),
                dbc.Card([
                    html.Legend("Total Green's"),
                    html.H5('R$ 759,22', id='green_balance', style={}),
                ], style={'padding-left': '25px', 'padding-top': '10px'}),
            ]),
        ], width=4),

        # Red
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Total Red's"),
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

                html.Legend('Per??odo de An??lise', style={'margin-top': '10px'}),
                dcc.DatePickerRange(
                    id='picker-date-config',
                    display_format='DD/MM/YYYY',
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
        dbc.Col(dbc.Card(dcc.Graph(id='graph-all'), style={'padding': '10px', 'margin': '10px'}), width=6),
        dbc.Col(dbc.Card(dcc.Graph(id='graph-greens'), style={'padding': '10px', 'margin-right': '10px'}), width=3),
        dbc.Col(dbc.Card(dcc.Graph(id='graph-reds'), style={'padding': '10px', 'margin-right': '20px'}), width=3),
    ]),
])


# =========  Callbacks  =========== #
# =========  Soma Greens  =========== #
@app.callback(
    [
        Output('dropdown-greens', 'options'),
        Output('dropdown-greens', 'value'),
        Output('green_balance', 'children')
    ],
    Input('store-greens', 'data')
)
def populate_dropdown_green(data):
    df = pd.DataFrame(data)
    value = df['Value'].sum()
    val = df.Market.unique().tolist()

    return [{'label': i, 'value': i} for i in val], val, f'R$ {value:.2f}'


# =========  Soma Reds  =========== #
@app.callback(
    [
        Output('dropdown-reds', 'options'),
        Output('dropdown-reds', 'value'),
        Output('red_balance', 'children')
    ],
    Input('store-reds', 'data')
)
def populate_dropdown_red(data):
    df = pd.DataFrame(data)
    value = df['Value'].sum()
    val = df.Market.unique().tolist()

    return [{'label': i, 'value': i} for i in val], val, f'-R$ {value:.2f}'


# =========  Soma Entradas  =========== #
@app.callback(
    Output('current_balance', 'children'),
    [
        Input('store-greens', 'data'),
        Input('store-reds', 'data')
    ]
)
def populate_entries_balance(greens, reds):
    df_greens = pd.DataFrame(greens)
    df_reds = pd.DataFrame(reds)
    value = df_greens['Value'].sum() - df_reds['Value'].sum()
    return f'R$ {value:.2f}'


# =========  Gr??fico crescimento da Banca  =========== #
@app.callback(
    Output('graph-entries', 'figure'),
    [
        Input('store-greens', 'data'),
        Input('store-reds', 'data'),
        Input('dropdown-greens', 'value'),
        Input('dropdown-reds', 'value'),
    ]
)
def update_output(data_greens, data_reds, greens, reds):
    df_greens = pd.DataFrame(data_greens).set_index('Date')[['Value']]
    df_gn = df_greens.groupby('Date').sum().rename(columns={'Value': 'Greens'})

    df_reds = pd.DataFrame(data_reds).set_index('Date')[['Value']]
    df_rd = df_reds.groupby('Date').sum().rename(columns={'Value': 'Reds'})

    df_acum = df_gn.join(df_rd, how='outer').fillna(0)
    df_acum['Acum'] = df_acum['Greens'] - df_acum['Reds']
    df_acum['Acum'] = df_acum['Acum'].cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(name="Fluxo de Caixa", x=df_acum.index, y=df_acum['Acum'], mode='lines+markers'))

    fig.update_layout(margin=graph_margin, height=300)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig


# =========  Gr??fico Green's x Red's  =========== #
@app.callback(
    Output('graph-all', 'figure'),
    [
        Input('store-greens', 'data'),
        Input('store-reds', 'data'),
        Input('dropdown-greens', 'value'),
        Input('dropdown-reds', 'value'),
        Input('picker-date-config', 'start_date'),
        Input('picker-date-config', 'end_date'),
    ]
)
def graph_a_view(data_greens, data_reds, greens, reds, start_date, end_date):
    df_gr = pd.DataFrame(data_greens)
    df_re = pd.DataFrame(data_reds)

    df_gr['Output'] = "Greens"
    df_re['Output'] = "Reds"
    df_final = pd.concat([df_gr, df_re])
    df_final['Date'] = pd.to_datetime(df_final['Date'])

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_final = df_final[(df_final['Date'] >= start_date) & (df_final['Date'] <= end_date)]
    df_final = df_final[(df_final['Market'].isin(greens)) | (df_final['Market'].isin(reds))]

    fig = px.bar(df_final, x='Date', y='Value', color='Output', barmode='group')
    fig.update_layout(margin=graph_margin, height=450)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig


# =========  Gr??fico Mercados Green's =========== #
@app.callback(
    Output('graph-greens', 'figure'),
    [
        Input('store-greens', 'data'),
        Input('dropdown-greens', 'value'),
    ]
)
def graph_greens_view(data_greens, greens):
    df_gr = pd.DataFrame(data_greens)
    df_gr = df_gr[df_gr['Market'].isin(greens)]

    fig = px.pie(df_gr, values=df_gr.Value, names=df_gr.Market, hole=0.2)
    fig.update_layout(title={'text': "Mercados Green's"})
    fig.update_layout(margin=graph_margin, height=450)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig


# =========  Gr??fico Mercados Red's =========== #
@app.callback(
    Output('graph-reds', 'figure'),
    [
        Input('store-reds', 'data'),
        Input('dropdown-reds', 'value'),
    ]
)
def graph_greens_view(data_reds, reds):
    df_re = pd.DataFrame(data_reds)
    df_re = df_re[df_re['Market'].isin(reds)]

    fig = px.pie(df_re, values=df_re.Value, names=df_re.Market, hole=0.2)
    fig.update_layout(title={'text': "Mercados Red's"})
    fig.update_layout(margin=graph_margin, height=450)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig
