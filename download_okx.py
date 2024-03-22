import requests
import pandas as pd

# Параметры для запроса
symbol = "TON-USDT"  # Пример торговой пары
period = "1D"  # Пример периода: 1 день
after = "1651104000000"  # Пример начальной даты в формате Unix timestamp (миллисекунды)
before = "1396800001"  # Пример конечной даты в формате Unix timestamp (миллисекунды)
limit = "100"  # Количество результатов

# Удаление лишней закрывающей фигурной скобки из URL
url = f"https://www.okx.com/api/v5/market/history-candles?instId={symbol}&after={after}&bar={period}&limit={limit}"

# Выполнение HTTP GET запроса
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    # Извлечение данных из JSON ответа
    data = response.json().get('data', [])

    if data:
        # Создаем DataFrame из полученных данных
        # Указываем правильное количество и названия столбцов согласно структуре ответа API
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'volume_in_base_currency',
                   'volume_in_quote_currency', 'confirm']
        df = pd.DataFrame(data, columns=columns)

        # Преобразуем timestamp из строки в datetime
        # Поскольку в вашем случае timestamp уже в правильном формате, этот шаг может быть не нужен
        # df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        # Если timestamp возвращается в виде Unix timestamp в миллисекундах, используйте следующую строку
        df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
        df['timestamp'] = df['timestamp'].dt.date
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%d-%m-%Y')

        # Выбираем только интересующие столбцы, если это необходимо
        df = df[['timestamp', 'close']]
        #df = df.iloc[::-1].reset_index(drop=True)

        print(df)
        # Предположим, df_final - это DataFrame, который вы хотите дописать в файл
        df.to_csv('data/csv/TON.csv', mode='a', index=False, header=False)

    else:
        print("Полученные данные пусты.")

else:
    print("Ошибка при выполнении запроса:", response.status_code)
