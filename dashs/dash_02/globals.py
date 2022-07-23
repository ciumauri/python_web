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
    data_structure = {
        'Value': [],
        'Date': [],
        'Odds': [],
        'Market': [],
        'Description': [],
    }
    df_greens = pd.DataFrame(data_structure)
    df_reds = pd.DataFrame(data_structure)
    df_greens.to_csv("datas/df_greens.csv")
    df_reds.to_csv("datas/df_reds.csv")

if "df_mkt_list.csv" in os.listdir():
    df_mkt_list = pd.read_csv("datas/df_mkt_list.csv", index_col=0, parse_dates=True)
    data_market_list = df_mkt_list.values.tolist()

else:
    data_market_list = {
        'Categoria': [
            'Back Favorito',
            'Back Zebra',
            'Lay Favorito',
            'Lay Zebra',
        ]
    }

df_mkt_list = pd.DataFrame(data_market_list)
df_mkt_list.to_csv("datas/df_mkt_list.csv")
