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
        html.Legend('Tabela de Entradas Green'),
        html.Div(id='table-entries-green', className='dbc'),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-entries-green', style={'margin-right': '20px'}),
        ], width=9),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Entradas Green"),
                    html.Legend("-R$ 366,28 ", id="value-entries-green", style={'font-size': '3rem'}),
                    html.H6("Total de Green's"),
                ], style={'text-align': 'center', 'padding-top': '30px'}),
            ], style={'margin-right': '20px'}),
        ], width=3),
    ]),
], style={'padding': '10px'})

# =========  Callbacks  =========== #
# Tabela
@app.callback(
    Output('table-entries-green', 'children'),
    [Input('store-greens', 'data')]
)
def print_table(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df.fillna('-')
    df.sort_values(by=['Date'], inplace=True, ascending=False)

    table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], editable=False, row_deletable=True, style_cell={'textAlign': 'center'}, style_data_conditional=[{'if': {'column_id': 'Market'}, 'width': '20%'}, {'if': {'column_id': 'Date'}, 'width': '20%'}, {'if': {'column_id': 'Value'}, 'width': '20%'}, {'if': {'column_id': 'Description'}, 'width': '40%'}], style_table={'overflowX': 'scroll'})
    return table

@app.callback(
    Output('bar-graph-entries-green', 'figure'),
    [Input('store-greens', 'data')]
)
def bar_graph(data):
    df = pd.DataFrame(data)
    df_grouped = df.groupby(['Market']).sum()[['Value']].reset_index()
    graph = px.bar(df_grouped, x='Market', y='Value', color='Market', barmode='group', height=400)
    graph.update_layout(title_text='Entradas Green', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return graph

@app.callback(
    Output('value-entries-green', 'children'),
    [Input('store-greens', 'data')]
)
def print_value(data):
    df = pd.DataFrame(data)
    return 'R$ ' + str(df['Value'].sum())
