from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask_login import current_user, LoginManager

from app import *
from pages import login, register, dashboard, extratos_green, extratos_red
from globals import *

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# =========  Layout  =========== #
app.layout = dbc.Container(children=[
    dcc.Store(id='store-greens', data=df_greens.to_dict()),
    dcc.Store(id='store-reds', data=df_reds.to_dict()),
    dcc.Store(id='store-mkt-list-green', data=df_mkt_list_green.to_dict()),
    dcc.Store(id='store-mkt-list-red', data=df_mkt_list_red.to_dict()),

    dbc.Row([
        dbc.Col([
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="login-state", data=""),
            dcc.Store(id="register-state", data=""),

            html.Div(id="page-content", style={"height": "100vh", "display": "flex", "justify-content": "center"})
        ]),
    ])
], fluid=True, style={"height": "100vh"})


# =========  Callbacks Index  =========== #
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.callback(Output("url", "pathname"),
              [
                  Input("login-state", "data"),
                  Input("register-state", "data")
              ])
def render_page_content(login_state, register_state):
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigg_id == 'login-state' and login_state == "success":
            return '/dashboard'
        if trigg_id == 'login-state' and login_state == "error":
            return '/login'

        elif trigg_id == 'register-state':
            print(register_state, register_state == '')
            if register_state == "":
                return '/login'
            else:
                return '/register'
    else:
        return '/'


@app.callback(Output("page-content", "children"),
              Input("url", "pathname"),
              [State("login-state", "data"), State("register-state", "data")])
def render_page_content(pathname, login_state, register_state):
    if pathname == "/login" or pathname == "/":
        return login.render_layout(login_state)

    if pathname == "/register":
        return register.render_layout(register_state)

    if pathname == "/dashboard":
        if current_user.is_authenticated:
            return dashboard.render_layout(current_user.username)
        else:
            # Não esquecer de retornar o login
            # return dashboard.render_layout(register_state)
            return dashboard.render_layout(register_state)

    if pathname == "/extratos_green":
        if current_user.is_authenticated:
            return extratos_green.render_layout(current_user.username)
        else:
            # Não esquecer de retornar o login
            # return dashboard.render_layout(register_state)
            return extratos_green.render_layout(register_state)

    if pathname == "/extratos_red":
        if current_user.is_authenticated:
            return extratos_red.render_layout(current_user.username)
        else:
            # Não esquecer de retornar o login
            # return dashboard.render_layout(register_state)
            return extratos_red.render_layout(register_state)


if __name__ == "__main__":
    app.run_server(port=8051, debug=True)
