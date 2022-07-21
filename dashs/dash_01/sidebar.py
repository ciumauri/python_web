from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO
from app import app

style_sidebar = style = {"box-shadow": "2px 2px 10px 0px rgba(10, 9, 7, 0.10)",
                         "margin": "10px",
                         "padding": "10px",
                         "height": "100vh"}

# =========  Layout  =========== #
layout = dbc.Card(
    [
        dbc.CardImg(src="/assets/images/logo_dark.png", top=True, style={"width": "80%", "margin-left": "auto", "margin-right": "auto"}),
        html.Hr(),
        html.P("A simple sidebar layout with navigation links", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Page1", href="/page1", active="exact"),
                dbc.NavLink("Page2", href="/page2", active="exact"),
                dbc.NavLink("Page3", href="/page3", active="exact"),
            ])
    ], style=style_sidebar
)
