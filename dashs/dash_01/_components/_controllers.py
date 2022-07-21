from dash import dcc, html
import dash_bootstrap_components as dbc

list_of_locations = {
    "All": 0,
    "Manhattan": 1,
    "Bronx": 2,
    "Brooklyn": 3,
    "Queens": 4,
    "Staten Island": 5
}

slider_size = [100, 500, 1000, 5000, 10000, 10000000]

controllers = dbc.Row([
    html.H3("Vendas de Imóveis - NYC", style={"margin-top": "100px"}),
    html.P("Utilize este dashboard para analisar vendas ocorridas na cidade de New York no período de 1 ano."),

    html.H4("""Distrito""", style={"margin-top": "25px", "margin-bottom": "15px"}),
    dcc.Dropdown(
        id="location-dropdown",
        options=[{"label": i, "value": j} for i, j in list_of_locations.items()],
        value=0,
        placeholder="Selecione um distrito"
    ),
    html.H4("""Metragem (m²)""", style={"margin-top": "20px", "margin-bottom": "15px"}),
    dcc.Slider(id="slider-square-size",
               min=0, max=4, marks={i: str(j) for i, j in enumerate(slider_size)}),

    html.H4("""Variável de Controle""", style={"margin-top": "20px", "margin-bottom": "15px"}),
    dcc.Dropdown(
        options=[
            {"label": "YEAR BUILT", "value": "YEAR BUILT"},
            {"label": "TOTAL UNITS", "value": "TOTAL UNITS"},
            {"label": "SALE PRICE", "value": "SALE PRICE"},
        ],
        value="SALE PRICE",
        id="dropdown-color")
])
