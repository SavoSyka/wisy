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
BTC_data = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Dec, 2017", "19 Jun, 2023")
BTC = pd.DataFrame(BTC_data)

BTC.columns = ['date', 'open', 'high', 'low', 'close', '5', '6', '7', '8', '9', '10', '11']
cols = [1,2,3,5,6,7,8,9,10,11]
BTC.drop (BTC.columns [cols], axis= 1 , inplace= True )

for i in range (0,2027):
    BTC.loc[i, 'date'] = datetime.utcfromtimestamp(BTC.loc[i, 'date'] / 1000).strftime('%d-%m-%Y')
    BTC.loc[i, 'close'] = float(BTC.loc[i, 'close'])

print(BTC.tail())

BTC.to_excel('data/BTC.xlsx', index=False)
BTC.to_csv('data/BTC.csv', index=False)
