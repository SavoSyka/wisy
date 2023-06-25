from binance import Client, ThreadedDepthCacheManager, ThreadedWebsocketManager
import pandas as pd
from datetime import datetime
import openpyxl
import numpy as np
from matplotlib import pyplot as plt
f = open('keys/api.txt', 'r')
apikey = f.read()
f = open('keys/secret.txt', 'r')
secret = f.read()
client = Client(apikey, secret)
name = 'ETH'
pair = name + 'USDT'
data = client.get_historical_klines(f'{pair}', Client.KLINE_INTERVAL_1DAY, "1 May, 2017", "23 Jun, 2023")
df = pd.DataFrame(data)

df.columns = ['date', 'open', 'high', 'low', 'close', '5', '6', '7', '8', '9', '10', '11']
cols = [1,2,3,5,6,7,8,9,10,11]
df.drop (df.columns [cols], axis= 1, inplace= True)
print(df.shape[0])
for i in range (0,df.shape[0]):
    df.loc[i, 'date'] = datetime.utcfromtimestamp(df.loc[i, 'date'] / 1000).strftime('%d-%m-%Y')
    df.loc[i, 'close'] = float(df.loc[i, 'close'])

print(df.tail())

df.to_excel(f'data/xlsx/{name}.xlsx', index=False)
df.to_csv(f'data/csv/{name}.csv', index=False)
