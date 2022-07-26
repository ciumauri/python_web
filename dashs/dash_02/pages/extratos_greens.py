from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import *

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from dash.exceptions import PreventUpdate


from components import _sidebar, _extratos


# =========  Layout  =========== #
def render_layout(username):
    template = dbc.Container([
        dbc.Row([
            dbc.Col([
                _sidebar.layout
            ], md=2),
            dbc.Col([
                _extratos.layout
            ], md=10),
        ]),

    ], fluid=True)
    return template

    # =========  Callbacks Page1  =========== #



