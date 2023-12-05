import pandas as pd
from src.pipelines.command import DatabaseSetup, Querying
from src.models.stocks import StockTrades

def read_csv(path):
    df = pd.read_csv(path)
    df.columns = [col.replace(' ', '_').lower() for col in df.columns]
    df['ticker'] = path.split('/')[-1].split('.')[0]

    return df


df = pd.concat(map(read_csv, ['./data/stocks/A.csv', './data/stocks/DIS.csv', './data/stocks/TSLA.csv']))
DatabaseSetup.run(df, StockTrades)
Querying.run(StockTrades)