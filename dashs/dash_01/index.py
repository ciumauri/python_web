import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from app import *
from _components._histogram import *
from _components._controllers import *
from pages import page1, page2, page3, login, register, data
import sidebar

# ==========================
# Data inport and preprocessing
# ==========================
df_data = pd.read_csv(os.getcwd() + os.sep
                      + 'dataset' + os.sep
                      + "cleaned_data.csv")
mean_lat = df_data['LATITUDE'].mean()
mean_lon = df_data['LONGITUDE'].mean()

df_data["size_m2"] = df_data["GROSS SQUARE FEET"] / 10.7639
df_data = df_data[df_data["YEAR BUILT"] > 0]
df_data["SALE DATE"] = pd.to_datetime(df_data["SALE DATE"])

df_data.loc[df_data["size_m2"] > 10000, "size_m2"] = 10000
df_data.loc[df_data["SALE PRICE"] > 50000000, "SALE PRICE"] = 50000000
df_data.loc[df_data["SALE PRICE"] < 100000, "SALE PRICE"] = 100000

# ==========================
# Layout
# ==========================

app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dcc.Location(id="url"),
            sidebar.layout
        ], md=2),

        dbc.Col([
            html.Div(id="page-content")
        ]),
    ], style={"padding": "0px"})
], fluid=True, )


# ==========================
# Callbacks
# ==========================
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/" or pathname == "/login":
        return login.layout

    if pathname == "/page1":
        return page1.layout

    if pathname == "/page2":
        return page2.layout

    if pathname == "/page3":
        return page3.layout


@app.callback([Output("hist-graph", "figure"), Output("map-graph", "figure")],
              [Input("location-dropdown", "value"),
               Input("slider-square-size", "value"),
               Input("dropdown-color", "value")])
def update_hist(location, square_size, color_map):
    if location is None:
        df_intermediate = df_data.copy()
    else:
        df_intermediate = df_data[df_data["BOROUGH"] == location] if location != 0 else df_data.copy()
        size_limit = slider_size[square_size] if square_size is not None else df_data["GROSS SQUARE FEET"].max()
        df_intermediate = df_intermediate[df_intermediate["GROSS SQUARE FEET"] <= size_limit]

    hist_fig = px.histogram(df_intermediate, x=color_map, opacity=0.75)
    hist_layout = go.Layout(
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        showlegend=False,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", )
    hist_fig.layout = hist_layout

    px.set_mapbox_access_token(open(os.getcwd() + os.sep + "keys" + os.sep + "mapbox_access_token").read())

    colors_rgb = px.colors.sequential.GnBu
    df_quantiles = df_data[color_map].quantile(np.linspace(0, 1, len(colors_rgb))).to_frame()
    df_quantiles = (df_quantiles - df_quantiles.min()) / (df_quantiles.max() - df_quantiles.min())
    df_quantiles["colors"] = colors_rgb
    df_quantiles.set_index(color_map, inplace=True)

    color_scale = [[i, j] for i, j in df_quantiles["colors"].iteritems()]

    map_fig = px.scatter_mapbox(df_intermediate, lat="LATITUDE", lon="LONGITUDE",
                                color=color_map, size="size_m2", size_max=10, zoom=9.5, opacity=0.4)
    map_fig.update_coloraxes(colorscale=color_scale)
    map_fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=mean_lat, lon=mean_lon)),
                          template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                          margin=go.layout.Margin(l=10, r=10, t=10, b=10))

    return hist_fig, map_fig


if __name__ == "__main__":
    app.run_server(port=8051, debug=True)
