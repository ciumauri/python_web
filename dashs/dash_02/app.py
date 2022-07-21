import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import sqlite3
from sqlalchemy import Table, create_engine

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os

estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
           "https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons", dbc.themes.PULSE]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.5/dbc.min.css"

load_figure_template(["PULSE"])
app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])
server = app.server
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True

conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')
db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


Users_tbl = Table('users', Users.metadata)

server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False)

db.init_app(server)


class Users(UserMixin, Users):
    pass

# Setup the LoginManager for the server
