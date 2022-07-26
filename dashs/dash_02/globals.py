import os

import pandas as pd

if ("df_greens.csv" in os.listdir()) and ("df_reds.csv" in os.listdir()):
    df_greens = pd.read_csv("datas/df_greens.csv", index_col=0, parse_dates=True)
    df_reds = pd.read_csv("datas/df_reds.csv", index_col=0, parse_dates=True)
    df_greens["Date"] = pd.to_datetime(df_greens["Date"])
    df_reds["Date"] = pd.to_datetime(df_reds["Date"])
    df_greens["Date"] = df_greens["Date"].apply(lambda x: x.date())
    df_reds["Date"] = df_reds["Date"].apply(lambda x: x.date())

else:
    data_structure_green = {
        'Value': [350.0, 292.0, 325.0],
        'Date': ["2022-07-24", "2022-07-23", "2022-07-22"],
        'Odds': [1.65, 1.50, 1.69],
        'Market': ["Back Favorito", "Lay Zebra", "Lay Favorito"],
        'Description': ["Brasil x Argentina", "Palmeiras x Internacional", "Vasco x Bahia"],
    }

    data_structure_red = {
        'Value': [150.0, 200.0, 125.0],
        'Date': ["2022-07-24", "2022-07-23", "2022-07-22"],
        'Odds': [1.65, 1.50, 1.69],
        'Market': ["Back Favorito", "Lay Zebra", "Lay Favorito"],
        'Description': ["Brasil x Argentina", "Palmeiras x Internacional", "Vasco x Bahia"],
    }

    df_greens = pd.DataFrame(data_structure_green)
    df_reds = pd.DataFrame(data_structure_red)
    df_greens.to_csv("datas/df_greens.csv")
    df_reds.to_csv("datas/df_reds.csv")

if ("df_mkt_list_green.csv" in os.listdir()) and ("df_mkt_list_red.csv" in os.listdir()):
    df_mkt_list_green = pd.read_csv("datas/df_mkt_list_green.csv", index_col=0, parse_dates=True)
    df_mkt_list_red = pd.read_csv("datas/df_mkt_list_red.csv", index_col=0, parse_dates=True)
    data_market_list_green = df_mkt_list_green.values.tolist()
    data_market_list_red = df_mkt_list_red.values.tolist()


else:
    data_market_list_green = {
        'Categoria': [
            'Back Favorito',
            'Back Zebra',
            'Lay Favorito',
            'Lay Zebra',
        ]
    }

    data_market_list_red = {
        'Categoria': [
            'Back Favorito',
            'Back Zebra',
            'Lay Favorito',
            'Lay Zebra',
        ]
    }

df_mkt_list_green = pd.DataFrame(data_market_list_green)
df_mkt_list_red = pd.DataFrame(data_market_list_red)
df_mkt_list_green.to_csv("datas/df_mkt_list_green.csv")
df_mkt_list_red.to_csv("datas/df_mkt_list_red.csv")
