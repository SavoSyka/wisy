import pandas as pd
from datetime import datetime
import openpyxl
import numpy as np
from matplotlib import pyplot as plt

BTC = pd.read_csv('data/csv/BTC.csv')
BTC_1 = pd.read_csv('data/csv/BTC_1.csv')
BTC_2 = pd.read_csv('data/csv/BTC_2.csv')
ETH = pd.read_csv('data/csv/ETH.csv')
XRP = pd.read_csv('data/csv/XRP.csv')

LTC_1 = pd.read_csv('data/csv/LTC_1.csv')
DOGE_1 = pd.read_csv('data/csv/DOGE_1.csv')
BCH_1 = pd.read_csv('data/csv/BCH_1.csv')
KAS = pd.read_csv('data/csv/KAS_ref.csv')
XMR_1 = pd.read_csv('data/csv/XMR_1.csv')

LTC_2 = pd.read_csv('data/csv/LTC_2.csv')
DOGE_2 = pd.read_csv('data/csv/DOGE_2.csv')
BCH_2 = pd.read_csv('data/csv/BCH_2.csv')
KAS = pd.read_csv('data/csv/KAS_ref.csv')
XMR_2 = pd.read_csv('data/csv/XMR_2.csv')

MATIC = pd.read_csv('data/csv/MATIC.csv')
ADA = pd.read_csv('data/csv/ADA.csv')
SOL = pd.read_csv('data/csv/SOL.csv')
#TON = pd.read_csv('data/csv/TON.csv')

LINK = pd.read_csv('data/csv/LINK.csv')
LDO = pd.read_csv('data/csv/LDO.csv')
MKR = pd.read_csv('data/csv/MKR.csv')
UNI = pd.read_csv('data/csv/UNI.csv')
AAVE = pd.read_csv('data/csv/AAVE.csv')
COMP = pd.read_csv('data/csv/COMP.csv')

ARB = pd.read_csv('data/csv/ARB.csv')
OP = pd.read_csv('data/csv/OP.csv')

# График без ребалансировки портфеля
usd = 0
usd_list = []

btc = 0
btc_list = []
btc_to_usd = []

ltc = 0
ltc_list = []
ltc_to_usd = []

doge = 0
doge_list = []
doge_to_usd = []

kas = 0
kas_list = []
kas_to_usd = []

bch = 0
bch_list = []
bch_to_usd = []

xmr = 0
xmr_list = []
xmr_to_usd = []

eth = 0
eth_list = []
eth_to_usd = []

xrp = 0
xrp_list = []
xrp_to_usd = []

date = []
close = []
SumValue = []
begin = 0
end = BTC.shape[0]
day = begin % 7
btc_kotleta = 27800/float(BTC.loc[0, 'close'])
btc_kotleta_usd = []
for i in range(begin, end):
    if i % 7 == day:
        usd += 100
        usd_list.append(usd)

        btc += 60 / float(BTC.loc[i, 'close'])
        btc_to_usd.append(btc * float(BTC.loc[i, 'close']))

        eth += 30 / float(ETH.loc[i, 'close'])
        eth_to_usd.append(eth * float(ETH.loc[i, 'close']))

        xrp += 20 / float(XRP.loc[i, 'close'])
        xrp_to_usd.append(xrp * float(XRP.loc[i, 'close']))

        btc_kotleta_usd.append(btc_kotleta*float(BTC.loc[i, 'close']))

        SumValue.append(eth * float(ETH.loc[i, 'close']) + btc * float(BTC.loc[i, 'close'])+ xrp * float(XRP.loc[i, 'close']))

        date.append(BTC.loc[i, 'date'])
        #close.append(BTC.loc[i, 'close'] * (28800 / BTC.loc[begin, 'close']))

# # График с ребалансировкой портфеля
# usd_rebalanced = 0
# usd_list_rebalanced = []
# btc_rebalanced = 0
# btc_list_rebalanced = []
# btc_to_usd_rebalanced = []
#
# eth_rebalanced = 0
# eth_list_rebalanced = []
# eth_to_usd_rebalanced = []
# date_rebalanced = []
# close_rebalanced = []
# SumValue_rebalanced = []
# rebalance_period = 90
# rebalance_counter = 0
#
# for i in range(begin, end):
#     if i % 7 == day:
#         usd_rebalanced += 100
#         usd_list_rebalanced.append(usd_rebalanced)
#
#         btc_rebalanced += 50 / float(BTC.loc[i, 'close'])
#         btc_list_rebalanced.append(btc_rebalanced)
#
#         btc_to_usd_rebalanced.append(btc_rebalanced * float(BTC.loc[i, 'close']))
#
#         eth_rebalanced += 50 / float(ETH.loc[i, 'close'])
#         eth_list_rebalanced.append(eth_rebalanced)
#
#         eth_to_usd_rebalanced.append(eth_rebalanced * float(ETH.loc[i, 'close']))
#
#         SumValue_rebalanced.append(eth_rebalanced * float(ETH.loc[i, 'close']) + btc_rebalanced * float(BTC.loc[i, 'close']))
#
#         date_rebalanced.append(BTC.loc[i, 'date'])
#         close_rebalanced.append(BTC.loc[i, 'close'] * (28800 / BTC.loc[begin, 'close']))
#
#     if rebalance_counter == rebalance_period:
#         total_value = btc_rebalanced * float(BTC.loc[i, 'close']) + eth_rebalanced * float(ETH.loc[i, 'close'])
#         target_btc = total_value / (2 * float(BTC.loc[i, 'close']))
#         target_eth = total_value / (2 * float(ETH.loc[i, 'close']))
#         btc_rebalanced = target_btc
#         eth_rebalanced = target_eth
#         # btc_list_rebalanced.append(btc_rebalanced)
#         # eth_list_rebalanced.append(eth_rebalanced)
#         # usd_list_rebalanced.append(usd_list_rebalanced[-1])
#         # btc_to_usd_rebalanced.append(btc_rebalanced * float(BTC.loc[i, 'close']))
#         # eth_to_usd_rebalanced.append(eth_rebalanced * float(ETH.loc[i, 'close']))
#         # date_rebalanced.append(BTC.loc[i, 'date'])
#         # SumValue_rebalanced.append(eth_rebalanced * float(ETH.loc[i, 'close']) + btc_rebalanced * float(BTC.loc[i, 'close']))
#         rebalance_counter = 0
#
#     rebalance_counter += 1
#
for i in range(0, len(btc_to_usd)):
    btc_to_usd[i] = btc_to_usd[i] * 2
    eth_to_usd[i] = eth_to_usd[i] * 2
#
# for i in range(0, len(btc_to_usd_rebalanced)):
#     btc_to_usd_rebalanced[i] = btc_to_usd_rebalanced[i] * 2
#     eth_to_usd_rebalanced[i] = eth_to_usd_rebalanced[i] * 2

# Построение графиков на одной фигуре
fig, ax = plt.subplots(figsize=(10, 6))

x_ticks_indices = range(0, len(date), 4)
x_ticks_labels = [date[i] for i in x_ticks_indices]

ax.set_title('ТОП 3')
ax.set_xlabel('Date')
ax.set_ylabel('USD')
ax.grid(True)

#ax.plot(date, btc_to_usd, label='BTC')
ax.plot(date, btc_kotleta_usd, label = 'one-time purchase BTC')
# ax.plot(date, eth_to_usd, label='ETH (No Rebalancing)')
ax.plot(date, SumValue, label='50% — BTC / 30% — ETH/ 20% — XRP')


# ax.plot(date_rebalanced, btc_to_usd_rebalanced, label='BTC (With Rebalancing)')
# ax.plot(date_rebalanced, eth_to_usd_rebalanced, label='ETH (With Rebalancing)')
#ax.plot(date_rebalanced, SumValue_rebalanced, label='BTC+ETH (With Rebalancing)', color='#00b894')
# ax.plot(date_rebalanced, usd_list_rebalanced, label='USD (With Rebalancing)')


ax.plot(date, usd_list, label='USD', )

plt.xticks(x_ticks_indices, x_ticks_labels, rotation=90)

plt.legend()

plt.tight_layout()

print('максимум деняк: ',max(SumValue), 'деняк в конце стратегии: ',SumValue[-1])
print('BTC ',max(btc_to_usd), btc_to_usd[-1])
print('ETH ',max(eth_to_usd), eth_to_usd[-1])
print('XRP ',max(xrp_to_usd), xrp_to_usd[-1])
print('дата пика: ',SumValue.index(max(SumValue)), date[SumValue.index(max(SumValue))])
print('вложено бачей: ',usd_list[-1])
print('вложено на пике: ', usd_list[SumValue.index(max(SumValue))])
print('\n')
# print(max(SumValue_rebalanced), SumValue_rebalanced[-1])
# print(max(btc_to_usd_rebalanced), btc_to_usd_rebalanced[-1])
# print(max(eth_to_usd_rebalanced), eth_to_usd_rebalanced[-1])
# print(SumValue_rebalanced.index(max(SumValue_rebalanced)), date[SumValue_rebalanced.index(max(SumValue_rebalanced))])
# print(usd_list_rebalanced[SumValue_rebalanced.index(max(SumValue_rebalanced))])
plt.savefig('top_3')
plt.show()


