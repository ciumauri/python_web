import os
from datetime import date, datetime

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
from app import *
from dash import dcc, html
from dash.dependencies import Input, Output, State
from globals import *
from this import d

# ========= Layout ========= #


layout = dbc.Col([
    dbc.Card(
        [
            html.H2("Minhas Apostas", className="text-primary",
                    style={"margin-left": "auto", "margin-right": "auto", }),
            dbc.CardImg(src="assets/images/logo_dark.png", top=True,
                        style={"width": "50%", "margin-left": "auto", "margin-right": "auto", }),
            html.Hr(),

            # ========= Seção Perfil ========= #
            dbc.Button(id='botao_avatar',
                       children=[
                           html.Img(src="assets/images/img_homem.png", id='avatar_change', alt="Avatar",
                                    className='perfil_avatar')
                       ]),

            # ========= Seção Novo ========= #
            dbc.Row([
                dbc.Col([
                    dbc.Button(color="success", id='open-new-green', children=['Green']),
                ], width=6),
                dbc.Col([
                    dbc.Button(color="danger", id='open-new-red', children=['Red']),
                ], width=6),
            ]),

            # ========= Modal Green ========= #
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Add New Green")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Descrição: '),
                            dbc.Input(id='new-green-desc', type='text', placeholder='Ex: Malmo FF x Djurgardens IF'),
                        ], width=6),
                        dbc.Col([
                            dbc.Label('Valor Apostado: '),
                            dbc.Input(id='value_green', type='number', value='', step=0.10, min=0.50,
                                      placeholder='Ex: R$100.00'),
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Data: '),
                            dcc.DatePickerSingle(
                                id='new-green-date',
                                min_date_allowed=date(2020, 1, 1),
                                max_date_allowed=date(2030, 12, 31),
                                date=datetime.today(),
                                display_format='DD/MM/YYYY',
                                style={"width": "100%"}
                            ),
                        ], width=4),

                        dbc.Col([
                            dbc.Label('Odd da Entrada: '),
                            dbc.Input(id='odd_green', type='number', value='', step=0.01, min=1.01, placeholder='1.01'),
                        ], width=4),

                        dbc.Col([
                            dbc.Label('Mercados : '),
                            dbc.Select(id='market-select',
                                       options=[{'label': i, 'value': i} for i in data_market_list['Categoria']],
                                       value=data_market_list['Categoria'][0]),
                        ], width=4),
                    ], style={"margin-top": "25px", "margin-bottom": "25px", }),

                    dbc.Row([
                        dbc.Accordion([
                            dbc.AccordionItem([
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend('Adicionar Mercado', style={'color': 'green'}),
                                        dbc.Input(id='add-new-market', type='text', placeholder='Ex: Over 1.5FT',
                                                  value=""),
                                        html.Hr(),
                                        dbc.Button(id='add-market-list', children=['Adicionar'],
                                                   className='btn btn-success',
                                                   style={'margin-top': '20px'}),
                                        html.Hr(),
                                        html.Div(id='market-list', style={'margin-top': '20px'}),
                                    ], width=6),

                                    dbc.Col([
                                        html.Legend('Remover Mercado', style={'color': 'red'}),
                                        dbc.Checklist(
                                            id='checklist-market',
                                            options=[{'label': i, 'value': i} for i in data_market_list['Categoria']],
                                            value=[],
                                            label_checked_style={'color': 'red'},
                                            input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},
                                        ),
                                        dbc.Button(id='remove-market-list', children=['Remove'],
                                                   className='btn btn-danger',
                                                   style={'margin-top': '20px'}),
                                    ], width=6),
                                ]),
                            ], title='Adicionar/Remover Mercados'),
                        ], flush=True, start_collapsed=True, id='market-accordion'),

                        html.Div(id='market-list-div', style={'padding-top': '20px'}),
                        dbc.ModalFooter([
                            dbc.Button(id='save-new-green', children=['Adicionar Green'], color='success'),
                            dbc.Popover(dbc.PopoverBody(children=['Green adicionado com sucesso!']),
                                        target='save-new-green', placement='left', trigger='click'),
                        ]),
                    ], style={"margin-top": "25px", "margin-bottom": "25px", }),
                ]),
            ], id="modal-new-green", size='lg', backdrop=True, centered=True, is_open=False,
                style={'background-color': 'rgba(17,140,79,0.05)'}),

            # ========= Modal Red ========= #
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Add New Red")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Descrição: '),
                            dbc.Input(id='new-red-desc', type='text', placeholder='Ex: Malmo FF x Djurgardens IF'),
                        ], width=6),
                        dbc.Col([
                            dbc.Label('Valor Apostado: '),
                            dbc.Input(id='value_red', type='number', value='', step=0.10, min=0.50,
                                      placeholder='Ex: R$100.00'),
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Data: '),
                            dcc.DatePickerSingle(
                                id='new-red-date',
                                min_date_allowed=date(2020, 1, 1),
                                max_date_allowed=date(2030, 12, 31),
                                date=datetime.today(),
                                display_format='DD/MM/YYYY',
                                style={"width": "100%"}
                            ),
                        ], width=4),

                        dbc.Col([
                            dbc.Label('Odd da Entrada: '),
                            dbc.Input(id='odd_red', type='number', value='', step=0.01, min=1.01, placeholder='1.01'),
                        ], width=4),

                        dbc.Col([
                            dbc.Label('Mercados : '),
                            dbc.Select(id='market-select',
                                       options=[{'label': i, 'value': i} for i in data_market_list['Categoria']],
                                       value=data_market_list['Categoria'][0]),
                        ], width=4),
                    ], style={"margin-top": "25px", "margin-bottom": "25px", }),

                    dbc.Row([
                        dbc.Accordion([
                            dbc.AccordionItem([
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend('Adicionar Mercado', style={'color': 'green'}),
                                        dbc.Input(id='add-new-market', type='text', placeholder='Ex: Over 1.5FT',
                                                  value=""),
                                        html.Hr(),
                                        dbc.Button(id='add-market-list', children=['Adicionar'],
                                                   className='btn btn-success',
                                                   style={'margin-top': '20px'}),
                                        html.Hr(),
                                        html.Div(id='market-list', style={'margin-top': '20px'}),
                                    ], width=6),

                                    dbc.Col([
                                        html.Legend('Remover Mercado', style={'color': 'red'}),
                                        dbc.Checklist(
                                            id='checklist-market',
                                            options=[{'label': i, 'value': i} for i in data_market_list],
                                            value=[],
                                            label_checked_style={'color': 'red'},
                                            input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},
                                        ),
                                        dbc.Button(id='remove-market-list', children=['Remove'],
                                                   className='btn btn-danger',
                                                   style={'margin-top': '20px'}),
                                    ], width=6),
                                ]),
                            ], title='Adicionar/Remover Mercados'),
                        ], flush=True, start_collapsed=True, id='market-accordion'),

                        html.Div(id='market-list-div', style={'padding-top': '20px'}),
                        dbc.ModalFooter([
                            dbc.Button(id='save-new-red', children=['Adicionar Red'], color='danger'),
                            dbc.Popover(dbc.PopoverBody(children=['Red adicionado com sucesso!']),
                                        target='save-new-red', placement='left', trigger='click'),
                        ]),
                    ], style={"margin-top": "25px", "margin-bottom": "25px", }),
                ]),
            ], id="modal-new-red", size='lg', backdrop=True, centered=True, is_open=False,
                style={'background-color': 'rgba(17,140,79,0.05)'}),

            # ========= Seção NAV ========= #
            html.Hr(),
            dbc.Nav([
                dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
                dbc.NavLink("Extratos", href="/extratos", active="exact"),
            ], vertical=True, pills=True, id="nav_buttons", style={"margin-bottom": "50px"}),
        ], className="card_sidebar align-self-center"),
], id="sidebar_container")


# =========  Callbacks  =========== #
# Pop-up Green
@app.callback(
    Output('modal-new-green', 'is_open'),
    Input('open-new-green', 'n_clicks'),
    State('modal-new-green', 'is_open')
)
def toggle_modal_green(n, is_open):
    if n:
        return not is_open


# Pop-up Red
@app.callback(
    Output('modal-new-red', 'is_open'),
    Input('open-new-red', 'n_clicks'),
    State('modal-new-red', 'is_open')
)
def toggle_modal_green(n, is_open):
    if n:
        return not is_open


# Salvar novo Green
@app.callback(
    Output('store-greens', 'data'),
    Input('save-new-green', 'n_clicks'),
    [
        State('new-green-desc', 'value'),
        State('value_green', 'value'),
        State('new-green-date', 'date'),
        State('odd_green', 'value'),
        State('market-select', 'value'),
        State('store-greens', 'data'),
    ]
)
def save_new_green(n, desc, value, date, odd, market, dict_greens):
    df_greens = pd.DataFrame(dict_greens)

    if n and not (value == "" or value is None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        market = market[0] if type(market) == list else market
        odd = round(float(odd), 2)

        df_greens.loc[df_greens.shape[0]] = [value, date, odd, market, desc]
        df_greens.to_csv('datas/df_greens.csv')

    data_return = df_greens.to_dict()
    return data_return

# Salvar novo Red
@app.callback(
    Output('store-reds', 'data'),
    Input('save-new-red', 'n_clicks'),
    [
        State('new-red-desc', 'value'),
        State('value_red', 'value'),
        State('new-red-date', 'date'),
        State('odd_red', 'value'),
        State('market-select', 'value'),
        State('store-reds', 'data'),
    ]
)
def save_new_red(n, desc, value, date, odd, market, dict_reds):
    df_reds = pd.DataFrame(dict_reds)

    if n and not (value == "" or value is None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        market = market[0] if type(market) == list else market
        odd = round(float(odd), 2)

        df_reds.loc[df_greens.shape[0]] = [value, date, odd, market, desc]
        df_reds.to_csv('datas/df_reds.csv')

    data_return = df_reds.to_dict()
    return data_return

# Add/Remove Mercados
@app.callback(
    [
    Output('market-select', 'options'),
    Output('checklist-market', 'options'),
    Output('checklist-market', 'value'),
    Output('store-mkt-list', 'data')],

    [Input('add-market-list', 'n_clicks'),
     Input('remove-market-list', 'n_clicks')],

    [State('add-new-market', 'value'),
     State('checklist-market', 'value'),
     State('store-mkt-list', 'data')]
)
def add_remove_market(n_add, n_remove, new_market, market_remove, dict_mkt_list):    

    data_market_list = list(dict_mkt_list['Categoria'].values())    

    if n_add and not (new_market == "" or new_market is None):
        data_market_list = data_market_list + [new_market] if new_market not in data_market_list else data_market_list
    
    if n_remove:
        if len(market_remove) > 0:
            data_market_list = [i for i in data_market_list if i not in market_remove]

    opt_market_list = [{'label': i, 'value': i} for i in data_market_list]
    df_mkt_list = pd.DataFrame(dict_mkt_list, columns=['Categoria'])
    df_mkt_list.to_csv('datas/df_mkt_list.csv')
    data_return = df_mkt_list.to_dict()

    return [opt_market_list, opt_market_list, [], data_return]
