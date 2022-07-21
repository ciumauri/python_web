import pandas as pd
import os

if ("df_greens.csv" in os.listdir()) and ("df_reds.csv" in os.listdir()):
    df_greens = pd.read_csv("df_greens.csv", index_col=0, parse_dates=True)
    df_reds = pd.read_csv("df_reds.csv", index_col=0, parse_dates=True)

else:
    data_structure = {
        'Description': [],
        'Date': [],
        'Market': [],
        'Value': [],
        'Odds': [],
    }
    df_greens = pd.DataFrame(data_structure)
    df_reds = pd.DataFrame(data_structure)
    df_greens.to_csv("datas/df_greens.csv")
    df_reds.to_csv("datas/df_reds.csv")

if "df_mkt_list.csv" in os.listdir():
    df_mkt_list = pd.read_csv("df_mkt_list.csv", index_col=0, parse_dates=True)
    data_market_list = df_mkt_list.values.tolist()

else:
    data_market_list = {
        'Description': [
            'Back Favorito',
            'Back Zebra',
            'Lay Favorito',
            'Lay Zebra',
            'Over 0.5HT',
            'Over 0.5FT',
            'Over 1.5FT',
            'Over 2.5FT',
            'Under 1.5FT',
            'Under 2.5FT',
            'Under 3.5FT',
            'Cantos Over',
            'Cantos Under',
            'Cantos Asiáticos',
            'Gols Asiáticos',
            'Handcap Asiático'
        ]}

df_mkt_list = pd.DataFrame(data_market_list)
df_mkt_list.to_csv("datas/df_mkt_list.csv")
