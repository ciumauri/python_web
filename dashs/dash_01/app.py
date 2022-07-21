import dash
import dash_bootstrap_components as dbc
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import configparser
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                suppress_callback_exceptions=True)
app.scripts.config.serve_locally = True
server = app.server