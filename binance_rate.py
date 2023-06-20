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
BTC_data = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Dec, 2017", "17 Jun, 2023")
BTC = pd.DataFrame(BTC_data)

BTC.columns = ['date', 'open', 'high', 'low', 'close', '5', '6', '7', '8', '9', '10', '11']
cols = [1,2,3,5,6,7,8,9,10,11]
BTC.drop (BTC.columns [cols], axis= 1 , inplace= True )

for i in range (0,2025):
    BTC.loc[i, 'date'] = datetime.utcfromtimestamp(BTC.loc[i, 'date'] / 1000).strftime('%d-%m-%Y')
    # BTC.loc[i, 'open'] = float(BTC.loc[i, 'open'])
    # BTC.loc[i, 'high'] = float(BTC.loc[i, 'high'])
    # BTC.loc[i, 'low'] = float(BTC.loc[i, 'low'])
    BTC.loc[i, 'close'] = float(BTC.loc[i, 'close'])
print(BTC.tail())

# BTC.to_excel('data/BTC_USDT_01122017-17062023.xlsx', index=False)
# BTC.to_csv('data/BTC_USDT_01122017-17062023.csv', index=False)


# ETH_data = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1DAY, "1 Dec, 2017", "17 Jun, 2023")
# ETH = pd.DataFrame(ETH_data)
#
# ETH.columns = ['date', 'open', 'high', 'low', 'close', '5', '6', '7', '8', '9', '10', '11']
#
# for i in range (0,2025):
#     ETH.loc[i, 'date'] = datetime.utcfromtimestamp(ETH.loc[i, 'date'] / 1000).strftime('%Y-%m-%d')
# print(ETH.tail())

# ETH.to_excel('data/ETH_USDT_01122017-17062023.xlsx', index=False)
# ETH.to_csv('data/TH_USDT_01122017-17062023.csv', index=False)

summ = 0
bts = 0
for i in range (0,2025):
    if i % 7 == 0:
        summ += 100
        bts += 100/float(BTC.loc[i, 'close'])

print('weekly investing from 01.12.2017 to 17.06.2023:')
print('dollars invested: ', summ)
print('BTC: ', bts)
print('dollars got: ', bts*float(BTC.loc[2024, 'close']))
#
# print('\n')
# summ = 0
# btc = 0
# for i in range (1105,2025):
#     if i % 7 == 0:
#         summ += 100
#         btc += 100/float(BTC.loc[i, 'close'])
#
# print('weekly investing from 08.12.2020 to 17.06.2023:')
# print('dollars invested: ', summ)
# print('BTC: ', btc)
# print('dollars got: ', btc*float(BTC.loc[2024, 'close']))
#
print('\n')
summ = 0
btc = 0
for i in range (1000,2025):
    if i % 7 == 0:
        summ += 100
        btc += 100/float(BTC.loc[i, 'close'])

print('weekly investing from 25.08.2020 to 17.06.2023:')
print('dollars invested: ', summ)
print('BTC: ', btc)
print('dollars got: ', btc*float(BTC.loc[2024, 'close']))
#
# print('\n')
# summ = 0
# btc = 0
# for i in range(0, 2025):
#     if i % 30 == 0:
#         summ += 100
#         btc += 100 / float(BTC.loc[i, 'close'])
#
# print('every 30 days investing from 01.12.2017 to 17.06.2023:')
# print('dollars invested: ', summ)
# print('BTC: ', btc)
# print('dollars got: ', btc * float(BTC.loc[2024, 'close']))

usd = 0
usd_list = []
btc = 0
btc_list = []
btc_to_usd = []
date = []

begin = 379
end = 1422
day = begin % 7
for i in range(begin, end):

    if i % 7 == day:
        usd += 100
        usd_list.append(usd)
        btc += 100 / float(BTC.loc[i, 'close'])
        btc_list.append(btc)
        btc_to_usd.append(btc*float(BTC.loc[i, 'close']))
        date.append(BTC.loc[i, 'date'])
        summ += 100
if date[-1] != BTC.loc[end, 'date']:
    date.append(BTC.loc[end, 'date'])
    btc_to_usd.append(btc*float(BTC.loc[end, 'close']))
    usd_list.append(usd_list[-1])
# print('\n')
# print(btc, usd, btc * float(BTC.loc[2024, 'close']), btc * float(BTC.loc[2023, 'close']))
# print(btc_to_usd)
# print('every 30 days investing from 01.12.2017 to 17.06.2023:')
# print('dollars invested: ', usd)
# print('BTC: ', btc)
# print('dollars got: ', btc * float(BTC.loc[2024, 'close']))
x_ticks_indices = range(0, len(date), 4)
x_ticks_labels = [date[i] for i in x_ticks_indices]
plt.xlabel('Date')
plt.ylabel('USD')
plt.grid(True)
plt.plot(date, btc_to_usd)
plt.plot(date, usd_list)
plt.xticks(x_ticks_indices, x_ticks_labels, rotation=90)



#plt.plot(list(BTC['date']), list(BTC['close']))

plt.show()



