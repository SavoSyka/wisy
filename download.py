from binance import Client, ThreadedDepthCacheManager, ThreadedWebsocketManager
import pandas as pd
from datetime import datetime
import openpyxl
import numpy as np
from matplotlib import pyplot as plt

apikey = 'YK84JUTz0tcfmOcghsm01YHCb73XK0Yx5KOAnoR2KbGta6EWrXo4pPm05t7KQPDV'

secret = 'feuSxzTxOL5K4NaCLbiISQrNeujuriNXqp3DFvfSQOoj002p0jslrKl7MzwxMszk'
client = Client(apikey, secret)
name = 'ADA'
pair = name + 'USDT'
data = client.get_historical_klines(f'{pair}', Client.KLINE_INTERVAL_1DAY, "21 Mar, 2021", "21 Mar, 2024")
df = pd.DataFrame(data)

df.columns = ['date', 'open', 'high', 'low', 'close', '5', '6', '7', '8', '9', '10', '11']
cols = [1,2,3,5,6,7,8,9,10,11]
df.drop (df.columns [cols], axis= 1, inplace= True)
print(df.shape[0])
for i in range (0,df.shape[0]):
    df.loc[i, 'close'] = float(df.loc[i, 'close'])
# Преобразование столбца 'date' к типу datetime, а затем к строке
df['date'] = pd.to_datetime(df['date'], unit='ms').dt.strftime('%d-%m-%Y')

print(df.tail())

df.to_excel(f'data/xlsx/{name}.xlsx', index=False)
df.to_csv(f'data/csv/{name}.csv', index=False)
