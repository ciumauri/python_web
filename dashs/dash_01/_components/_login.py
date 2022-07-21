from dash import html, dcc
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


card_style = {
    'width: 300px'
    'min-height: 300px'
    'padding-top: 25px'
    'padding-right: 25px'
    'padding-left: 25px'
    'align-items: center'
}

login = dbc.Card([
    html.Legend("Login"),
], style=card_style)


