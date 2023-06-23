import pandas as pd
from datetime import datetime
import openpyxl
import numpy as np
from matplotlib import pyplot as plt

BTC = pd.read_csv('data/csv/BTC.csv')
ETH = pd.read_csv('data/csv/ETH.csv')

# График без ребалансировки портфеля
usd = 0
usd_list = []
btc = 0
btc_list = []
btc_to_usd = []

eth = 0
eth_list = []
eth_to_usd = []
date = []
close = []
SumValue = []
begin = 123
end = BTC.shape[0]
day = begin % 7
for i in range(begin, end):
    if i % 7 == day:
        usd += 100
        usd_list.append(usd)

        btc += 50 / float(BTC.loc[i, 'close'])
        btc_list.append(btc)

        btc_to_usd.append(btc * float(BTC.loc[i, 'close']))

        eth += 50 / float(ETH.loc[i, 'close'])
        eth_list.append(eth)

        eth_to_usd.append(eth * float(ETH.loc[i, 'close']))

        SumValue.append(eth * float(ETH.loc[i, 'close']) + btc * float(BTC.loc[i, 'close']))

        date.append(BTC.loc[i, 'date'])
        close.append(BTC.loc[i, 'close'] * (28800 / BTC.loc[begin, 'close']))

# График с ребалансировкой портфеля
usd_rebalanced = 0
usd_list_rebalanced = []
btc_rebalanced = 0
btc_list_rebalanced = []
btc_to_usd_rebalanced = []

eth_rebalanced = 0
eth_list_rebalanced = []
eth_to_usd_rebalanced = []
date_rebalanced = []
close_rebalanced = []
SumValue_rebalanced = []
rebalance_period = 30
rebalance_counter = 0

for i in range(begin, end):
    if i % 7 == day:
        usd_rebalanced += 100
        usd_list_rebalanced.append(usd_rebalanced)

        btc_rebalanced += 50 / float(BTC.loc[i, 'close'])
        btc_list_rebalanced.append(btc_rebalanced)

        btc_to_usd_rebalanced.append(btc_rebalanced * float(BTC.loc[i, 'close']))

        eth_rebalanced += 50 / float(ETH.loc[i, 'close'])
        eth_list_rebalanced.append(eth_rebalanced)

        eth_to_usd_rebalanced.append(eth_rebalanced * float(ETH.loc[i, 'close']))

        SumValue_rebalanced.append(eth_rebalanced * float(ETH.loc[i, 'close']) + btc_rebalanced * float(BTC.loc[i, 'close']))

        date_rebalanced.append(BTC.loc[i, 'date'])
        close_rebalanced.append(BTC.loc[i, 'close'] * (28800 / BTC.loc[begin, 'close']))

    if rebalance_counter == rebalance_period:
        total_value = btc_rebalanced * float(BTC.loc[i, 'close']) + eth_rebalanced * float(ETH.loc[i, 'close'])
        target_btc = total_value / (2 * float(BTC.loc[i, 'close']))
        target_eth = total_value / (2 * float(ETH.loc[i, 'close']))
        btc_rebalanced = target_btc
        eth_rebalanced = target_eth
        # btc_list_rebalanced.append(btc_rebalanced)
        # eth_list_rebalanced.append(eth_rebalanced)
        # usd_list_rebalanced.append(usd_list_rebalanced[-1])
        # btc_to_usd_rebalanced.append(btc_rebalanced * float(BTC.loc[i, 'close']))
        # eth_to_usd_rebalanced.append(eth_rebalanced * float(ETH.loc[i, 'close']))
        # date_rebalanced.append(BTC.loc[i, 'date'])
        # SumValue_rebalanced.append(eth_rebalanced * float(ETH.loc[i, 'close']) + btc_rebalanced * float(BTC.loc[i, 'close']))
        rebalance_counter = 0

    rebalance_counter += 1

for i in range(0, len(btc_to_usd)):
    btc_to_usd[i] = btc_to_usd[i] * 2
    eth_to_usd[i] = eth_to_usd[i] * 2

for i in range(0, len(btc_to_usd_rebalanced)):
    btc_to_usd_rebalanced[i] = btc_to_usd_rebalanced[i] * 2
    eth_to_usd_rebalanced[i] = eth_to_usd_rebalanced[i] * 2

# Построение графиков на одной фигуре
fig, ax = plt.subplots(figsize=(10, 6))

x_ticks_indices = range(0, len(date), 4)
x_ticks_labels = [date[i] for i in x_ticks_indices]

ax.set_title('Portfolio Performance Comparison')
ax.set_xlabel('Date')
ax.set_ylabel('USD')
ax.grid(True)

# ax.plot(date, btc_to_usd, label='BTC (No Rebalancing)')
# ax.plot(date, eth_to_usd, label='ETH (No Rebalancing)')
ax.plot(date, SumValue, label='BTC+ETH (No Rebalancing)', color = 'orange')


# ax.plot(date_rebalanced, btc_to_usd_rebalanced, label='BTC (With Rebalancing)')
# ax.plot(date_rebalanced, eth_to_usd_rebalanced, label='ETH (With Rebalancing)')
ax.plot(date_rebalanced, SumValue_rebalanced, label='BTC+ETH (With Rebalancing)', color='#00b894')
# ax.plot(date_rebalanced, usd_list_rebalanced, label='USD (With Rebalancing)')


ax.plot(date, usd_list, label='USD', )

plt.xticks(x_ticks_indices, x_ticks_labels, rotation=90)

plt.legend()

plt.tight_layout()

print(max(SumValue), SumValue[-1])
print(max(btc_to_usd), btc_to_usd[-1])
print(max(eth_to_usd), eth_to_usd[-1])
print(SumValue.index(max(SumValue)), date[SumValue.index(max(SumValue))])
print(usd_list[SumValue.index(max(SumValue))])
print('\n')
print(max(SumValue_rebalanced), SumValue_rebalanced[-1])
print(max(btc_to_usd_rebalanced), btc_to_usd_rebalanced[-1])
print(max(eth_to_usd_rebalanced), eth_to_usd_rebalanced[-1])
print(SumValue_rebalanced.index(max(SumValue_rebalanced)), date[SumValue_rebalanced.index(max(SumValue_rebalanced))])
print(usd_list_rebalanced[SumValue_rebalanced.index(max(SumValue_rebalanced))])

plt.show()


