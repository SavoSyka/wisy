import pandas as pd

df = pd.read_csv('data/csv/ETH_1502913600-1687550399_graph_coinmarketcap.csv')


df['date'] = df['open;high;low;close;volume;marketCap;timestamp'].str.split(';').str.get(6)
df['cap'] = df['open;high;low;close;volume;marketCap;timestamp'].str.split(';').str.get(5)

del df[df.columns[0]]

for i in range (0,df.shape[0]):
    df.loc[i, 'date'] =  df.loc[i, 'date'][1:11]


df.to_csv('data/csv/ETH_cap.csv', index=False)
print(df.columns.values.tolist())
print(df.tail())