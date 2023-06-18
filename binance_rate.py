from binance import Client, ThreadedDepthCacheManager, ThreadedWebsocketManager
import pandas as pd
from datetime import datetime
import openpyxl
import numpy as np
from matplotlib import pyplot as plt
apikey = 'L9unNk9gLdXRQnwo869ZptQONUW7kwfZktfjg2YXMrhdlCB4LI5Ba2pJ2mzo4X0b'
secret = 'au1XYYo13c6YVmZY8XKzelYxA6GRZY5DyJOrd73Nkmtesm7gA8C8UT7geFlQ9WpN'
client = Client(apikey, secret)
BTC_data = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Dec, 2017", "17 Jun, 2023")
BTC = pd.DataFrame(BTC_data)

BTC.columns = ['date', 'open', 'high', 'low', 'close', '5', '6', '7', '8', '9', '10', '11']

for i in range (0,2025):
    BTC.loc[i, 'date'] = datetime.utcfromtimestamp(BTC.loc[i, 'date'] / 1000).strftime('%Y-%m-%d')
print(BTC.tail())

BTC.to_excel('BTC_USDT_01122017-17062023.xlsx', index=False)
BTC.to_csv('BTC_USDT_01122017-17062023.csv', index=False)


ETH_data = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1DAY, "1 Dec, 2017", "17 Jun, 2023")
ETH = pd.DataFrame(ETH_data)

ETH.columns = ['date', 'open', 'high', 'low', 'close', '5', '6', '7', '8', '9', '10', '11']

for i in range (0,2025):
    ETH.loc[i, 'date'] = datetime.utcfromtimestamp(ETH.loc[i, 'date'] / 1000).strftime('%Y-%m-%d')
print(ETH.tail())

ETH.to_excel('ETH_USDT_01122017-17062023.xlsx', index=False)
ETH.to_csv('ETH_USDT_01122017-17062023.csv', index=False)