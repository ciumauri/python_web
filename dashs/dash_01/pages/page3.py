from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash

# ==========================
# Layout
# ==========================
layout = dbc.Container(children=[
    dbc.Row(children=[
        dbc.Col(children=[
            html.H1("Page 3"),
        ]),
        dbc.Col(children=[]),
    ]),

], fluid=True, style={"padding": "0px"})

# ==========================
# Callbacks
# ==========================