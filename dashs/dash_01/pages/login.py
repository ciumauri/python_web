from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash

from _components._login import login

# ==========================
# Layout
# ==========================
layout = dbc.Container(children=[
    dbc.Row(children=[
        dbc.Col([login], md=12),
    ]),

], fluid=True, style={"padding": "0px"})

# ==========================
# Callbacks
# ==========================
