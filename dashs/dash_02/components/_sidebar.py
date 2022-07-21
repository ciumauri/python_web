import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import *
from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd

from globals import *

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
                                       options=[{'label': i, 'value': i} for i in data_market_list['Description']],
                                       value=data_market_list['Description'][0]),
                        ], width=4),
                    ], style={"margin-top": "25px", "margin-bottom": "25px", }),

                    dbc.Row([
                        dbc.Accordion([
                            dbc.AccordionItem([
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend('Adicionar Mercado', style={'color': 'green'}),
                                        dbc.Input(id='new-market', type='text', placeholder='Ex: Over 1.5FT',
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
                                            options=[],
                                            value=[],
                                            label_checked_style={'color': 'red'},
                                            input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},
                                        ),
                                        dbc.Button(id='remove-market', children=['Remove'],
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
                                       options=[{'label': i, 'value': i} for i in data_market_list['Description']],
                                       value=data_market_list['Description'][0]),
                        ], width=4),
                    ], style={"margin-top": "25px", "margin-bottom": "25px", }),

                    dbc.Row([
                        dbc.Accordion([
                            dbc.AccordionItem([
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend('Adicionar Mercado', style={'color': 'green'}),
                                        dbc.Input(id='new-market', type='text', placeholder='Ex: Over 1.5FT',
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
                                            options=[],
                                            value=[],
                                            label_checked_style={'color': 'red'},
                                            input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},
                                        ),
                                        dbc.Button(id='remove-market', children=['Remove'],
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
def open_modal_green(n, is_open):
    if n:
        return not is_open


# Pop-up Red
@app.callback(
    Output('modal-new-red', 'is_open'),
    Input('open-new-red', 'n_clicks'),
    State('modal-new-red', 'is_open')
)
def open_modal_green(n, is_open):
    if n:
        return not is_open
