import pandas as pd

# Загрузка данных
BTC = pd.read_csv('data/csv/BTC.csv')
ETH = pd.read_csv('data/csv/ETH.csv')
BNB = pd.read_csv('data/csv/BNB.csv')
TRX = pd.read_csv('data/csv/TRX.csv')
ADA = pd.read_csv('data/csv/ADA.csv')
LTC = pd.read_csv('data/csv/LTC.csv')
SOL = pd.read_csv('data/csv/SOL.csv')
MATIC = pd.read_csv('data/csv/MATIC.csv')
XRP = pd.read_csv('data/csv/XRP.csv')
TON = pd.read_csv('data/csv/TON_0.csv')

# Инициализация переменных для USD и каждой криптовалюты
usd = 0
usd_list = []



tokens_with_TON = {
    'BTC': {'amount': 0, 'to_usd': []},
    'ETH': {'amount': 0, 'to_usd': []},
    'BNB': {'amount': 0, 'to_usd': []},
    'TRX': {'amount': 0, 'to_usd': []},
    'ADA': {'amount': 0, 'to_usd': []},
    'LTC': {'amount': 0, 'to_usd': []},
    'SOL': {'amount': 0, 'to_usd': []},
    'MATIC': {'amount': 0, 'to_usd': []},
    'XRP': {'amount': 0, 'to_usd': []},
    'TON': {'amount': 0, 'to_usd': []}

}

# Допустим, у нас есть общая сумма USD для инвестиций каждую неделю и пропорции для каждой криптовалюты
weekly_investment = 304.6
investment_ratios_before_TON = {
    'BTC': 0.17,
    'ETH': 0.16,
    'BNB': 0.11,
    'TRX': 0.11,
    'ADA': 0.06,
    'LTC': 0.06,
    'SOL': 0.11,
    'MATIC': 0.11,
    'XRP': 0.11
}

investment_ratios_with_TON = {
    'BTC': 0.15,
    'ETH': 0.15,
    'BNB': 0.1,
    'TRX': 0.1,
    'ADA': 0.05,
    'LTC': 0.05,
    'SOL': 0.1,
    'MATIC': 0.1,
    'XRP': 0.1,
    'TON': 0.1
}
day_counter = 0
#print(TON.loc[403, 'close'])

for i in range(len(BTC)):
    if day_counter % 7 == 0:  # Проверяем, является ли текущий день днем инвестиции
        usd += weekly_investment
        usd_list.append(usd)
        if TON.loc[i, 'close'] == 0.0:
            #print(TON.loc[i, 'close'], '--  without TON')
            for token, data in tokens_with_TON.items():
                if token == 'TON':
                    data['amount'] = 0
                    data['to_usd'].append(0)
                else:
                    df = eval(token)  # Получаем DataFrame для токена
                    if i < len(df):  # Проверяем, чтобы индекс не вышел за пределы длины DataFrame
                        amount = (weekly_investment * investment_ratios_before_TON[token]) / float(df.loc[i, 'close'])
                        data['amount'] += amount
                        data['to_usd'].append(data['amount'] * float(df.loc[i, 'close']))


        else:
            #print(TON.loc[i, 'close'])
            for token, data in tokens_with_TON.items():
                df = eval(token)  # Получаем DataFrame для токена
                if i < len(df):  # Проверяем, чтобы индекс не вышел за пределы длины DataFrame
                    amount = (weekly_investment * investment_ratios_with_TON[token]) / float(df.loc[i, 'close'])
                    data['amount'] += amount
                    data['to_usd'].append(data['amount'] * float(df.loc[i, 'close']))
    day_counter += 1  # Увеличиваем счетчик дней после каждой итерации

# for i in range(len(TON)):
#     if day_counter % 7 == 0:  # Проверяем, является ли текущий день днем инвестиции
#         usd += weekly_investment
#         usd_list.append(usd)
#
#         for token, data in tokens_with_TON.items():
#             df = eval(token)  # Получаем DataFrame для токена
#             if i < len(df):  # Проверяем, чтобы индекс не вышел за пределы длины DataFrame
#                 amount = (weekly_investment * investment_ratios_with_TON[token]) / float(df.loc[i, 'close'])
#                 data['amount'] += amount
#                 data['to_usd'].append(data['amount'] * float(df.loc[i, 'close']))

    day_counter += 1  # Увеличиваем счетчик дней после каждой итерации
print(len(tokens_with_TON['TON']['to_usd']))
investment_dates = BTC['date'][0::7][:len(usd_list)]  # Пример для получения дат инвестиций
portfolio_value = [sum(value) for value in zip(*[data['to_usd'] for token, data in tokens_with_TON.items()])]
investment_dates = pd.to_datetime(investment_dates, dayfirst=True)

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd

# Настройка стиля с помощью Seaborn
sns.set(style="whitegrid")
print(len( pd.to_datetime(investment_dates)),len(investment_dates), len(portfolio_value), len(usd_list))
# for i in range(len(portfolio_value)):
#     print(i, ' : ', portfolio_value[i])
# Создание DataFrame для построения графика
data_for_plot = pd.DataFrame({
    'Дата': pd.to_datetime(investment_dates),
    'Стоимость портфеля': portfolio_value,
    'Инвестировано USD': usd_list
})

# Построение графика
plt.figure(figsize=(12, 6))

# График стоимости портфеля
sns.lineplot(x='Дата', y='Стоимость портфеля', data=data_for_plot, label='Стоимость портфеля', marker='o')

# График инвестированных средств
sns.lineplot(x='Дата', y='Инвестировано USD', data=data_for_plot, label='Инвестировано USD')

# Настройка форматирования оси X
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))  # Каждые три месяца
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Поворот меток даты на оси X
plt.xticks(rotation=45)

# Добавление подписей и заголовка
plt.xlabel('Дата')
plt.ylabel('Стоимость, USD')
plt.title('Динамика инвестиционного портфеля топ 10')
plt.legend()

# Установка сетки
plt.grid(True)
plt.savefig('TOP_10.png', format='png', dpi=300, bbox_inches='tight', transparent=False)

plt.tight_layout()
plt.show()
print(portfolio_value)