from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash

from _components._map import map
from _components._histogram import hist
from _components._controllers import controllers

# ==========================
# Layout
# ==========================
layout = dbc.Container(children=[
    dbc.Row(children=[
        dbc.Col([controllers], md=3),
        dbc.Col([map, hist], md=9)
    ]),

], fluid=True, style={"padding": "0px"})

# ==========================
# Callbacks
# ==========================

