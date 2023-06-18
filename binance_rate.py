from binance import Client, ThreadedDepthCacheManager, ThreadedWebsocketManager
import pandas as pd
from datetime import datetime
import openpyxl
import numpy as np
from matplotlib import pyplot as plt
apikey = 'L9unNk9gLdXRQnwo869ZptQONUW7kwfZktfjg2YXMrhdlCB4LI5Ba2pJ2mzo4X0b'
secret = 'au1XYYo13c6YVmZY8XKzelYxA6GRZY5DyJOrd73Nkmtesm7gA8C8UT7geFlQ9WpN'
client = Client(apikey, secret)
data = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Dec, 2017", "17 Jun, 2023")
BTC = pd.DataFrame(data)

BTC.columns = ['date', 'open', 'high', 'low', 'close', '5', '6', '7', '8', '9', '10', '11']


# ts = df.loc[0,'date']
# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
# print(ts)
for i in range (0,2025):
    BTC.loc[i, 'date'] = datetime.utcfromtimestamp(BTC.loc[i, 'date'] / 1000).strftime('%Y-%m-%d')
print(BTC.tail())
#print(datetime.fromtimestamp(df.loc[0,'date']))
# ts = int('1512086400')
# print(df.loc[0,'date']/1000)
# print(datetime.utcfromtimestamp(df.loc[0,'date']/1000).strftime('%Y-%m-%d'))




BTC.to_excel('BTC_USDT_01122017-17062023.xlsx', index=False)
BTC.to_csv('BTC_USDT_01122017-17062023.csv', index=False)