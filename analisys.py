import os
from pathlib import Path
from typing import Dict

import pandas as pd
from binance import Client
from dotenv import load_dotenv
from matplotlib import pyplot as plt

DATA_DIR = Path('data/csv')
DEFAULT_ALLOCATION = {'BTC': 50, 'ETH': 30, 'XRP': 20}
WEEKLY_INVESTMENT = 100
load_dotenv()
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
QUOTE_ASSET = os.getenv('QUOTE_ASSET', 'USDT')

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        if not API_KEY or not API_SECRET:
            raise RuntimeError('Отсутствуют Binance API ключи. Задайте BINANCE_API_KEY и BINANCE_API_SECRET в .env')
        _client = Client(API_KEY, API_SECRET)
    return _client


def load_price_history(token: str) -> pd.DataFrame | None:
    path = DATA_DIR / f'{token}.csv'
    if not path.exists():
        return None
    df = pd.read_csv(path)
    df['date_dt'] = pd.to_datetime(df['date'], dayfirst=True)
    return df


def parse_allocation(raw: str) -> dict[str, float]:
    allocation: dict[str, float] = {}
    for part in raw.split(','):
        if ':' not in part:
            raise ValueError('Используйте формат TOKEN:процент')
        token, share = part.split(':', 1)
        token = token.strip().upper()
        if not token:
            raise ValueError('Не заполнено имя токена')
        try:
            percent = float(share.replace('%', '').strip())
        except ValueError:
            raise ValueError(f'Не удалось прочитать процент для {token}')
        if percent <= 0:
            raise ValueError('Доли должны быть больше 0')
        allocation[token] = percent
    total = sum(allocation.values())
    if abs(total - 100) > 1e-6:
        raise ValueError(f'Сумма долей должна быть 100%, сейчас {total}')
    return allocation


def download_history(token: str, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    client = get_client()
    os.makedirs(DATA_DIR, exist_ok=True)
    pair = f'{token}{QUOTE_ASSET}'
    start = start_date.strftime('%d %b, %Y')
    end = end_date.strftime('%d %b, %Y')
    print(f'Загружаю {pair} с {start} по {end}...')
    data = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, start, end)
    if not data:
        raise RuntimeError(f'Binance не вернул данных для {pair}')
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', '5', '6', '7', '8', '9', '10', '11'])
    df = df[['date', 'close']]
    df['close'] = df['close'].astype(float)
    df['date'] = pd.to_datetime(df['date'], unit='ms').dt.strftime('%d-%m-%Y')
    df['date_dt'] = pd.to_datetime(df['date'], dayfirst=True)
    output_path = DATA_DIR / f'{token}.csv'
    df.to_csv(output_path, index=False)
    print(f' - сохранено в {output_path}')
    return df


def ensure_data(
    token: str,
    df: pd.DataFrame | None,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
) -> pd.DataFrame:
    if df is None:
        df = download_history(token, start_date, end_date)
    start_available = df['date_dt'].iloc[0]
    end_available = df['date_dt'].iloc[-1]
    if start_date < start_available or end_date > end_available:
        df = download_history(token, start_date, end_date)
    return df


def default_dates(df: pd.DataFrame | None) -> tuple[pd.Timestamp, pd.Timestamp]:
    if df is not None:
        return df['date_dt'].iloc[0], df['date_dt'].iloc[-1]
    today = pd.Timestamp.today().normalize()
    return today - pd.Timedelta(days=365), today


# ... rest of file unchanged until prompt allocation definitions ...
    allocation: dict[str, float] = {}
    for part in raw.split(','):
        if ':' not in part:
            raise ValueError('Используйте формат TOKEN:процент')
        token, share = part.split(':', 1)
        token = token.strip().upper()
        if not token:
            raise ValueError('Не заполнено имя токена')
        try:
            percent = float(share.replace('%', '').strip())
        except ValueError:
            raise ValueError(f'Не удалось прочитать процент для {token}')
        if percent <= 0:
            raise ValueError('Доли должны быть больше 0')
        allocation[token] = percent
    total = sum(allocation.values())
    if abs(total - 100) > 1e-6:
        raise ValueError(f'Сумма долей должна быть 100%, сейчас {total}')
    return allocation


def prompt_allocation() -> tuple[dict[str, float], Dict[str, pd.DataFrame | None]]:
    default_str = ', '.join(f'{token}:{share}' for token, share in DEFAULT_ALLOCATION.items())
    while True:
        raw = input(f'Укажите токены и доли (формат BTC:50,ETH:30,...) [{default_str}]: ').strip()
        try:
            allocation = parse_allocation(raw) if raw else DEFAULT_ALLOCATION
            dataframes = {token: load_price_history(token) for token in allocation}
            return {token: share / 100 for token, share in allocation.items()}, dataframes
        except ValueError as exc:
            print(f'Ошибка: {exc}')
            print('Попробуйте ещё раз.')


def prompt_date(message: str, default_value: pd.Timestamp) -> pd.Timestamp:
    default_str = default_value.strftime('%d-%m-%Y')
    while True:
        user_input = input(f'{message} [{default_str}]: ').strip()
        if not user_input:
            return default_value
        try:
            return pd.to_datetime(user_input, dayfirst=True)
        except ValueError:
            print('Не удалось распознать дату. Используйте формат ДД-ММ-ГГГГ, например 01-12-2025.')


def prompt_date_range(default_start: pd.Timestamp, default_end: pd.Timestamp) -> tuple[pd.Timestamp, pd.Timestamp]:
    while True:
        start = prompt_date('Введите начальную дату', default_start)
        end = prompt_date('Введите конечную дату', default_end)
        if start > end:
            print('Начальная дата должна быть раньше конечной.')
            continue
        return start, end


def build_chart(dates, lump_values, portfolio_values, usd_list, allocation_label, lump_label):
    fig, ax = plt.subplots(figsize=(10, 6))
    x_ticks_indices = range(0, len(dates), max(1, len(dates) // 10))
    x_ticks_labels = [dates[i] for i in x_ticks_indices]

    ax.set_title('DCA анализ')
    ax.set_xlabel('Дата')
    ax.set_ylabel('USD')
    ax.grid(True)

    ax.plot(dates, lump_values, label=lump_label)
    ax.plot(dates, portfolio_values, label=allocation_label)
    ax.plot(dates, usd_list, label='Инвестировано USD')

    plt.xticks(x_ticks_indices, x_ticks_labels, rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.savefig('top_3')
    plt.show()


def main():
    allocation, dfs = prompt_allocation()
    reference_token = next(iter(allocation))
    default_start, default_end = default_dates(dfs[reference_token])
    start_date, end_date = prompt_date_range(default_start, default_end)

    dfs = {
        token: ensure_data(token, dfs.get(token), start_date, end_date)
        for token in allocation
    }

    usd = 0
    usd_list = []
    portfolio_values = []
    investment_dates = []

    token_state = {token: {'amount': 0.0, 'values': []} for token in allocation}
    lump_token = reference_token
    lump_prices: list[float] = []

    reference_dates = dfs[reference_token]['date_dt']
    price_lookup = {
        token: df.set_index('date_dt')['close']
        for token, df in dfs.items()
    }
    mask = (reference_dates >= start_date) & (reference_dates <= end_date)
    indices = reference_dates[mask].index.tolist()
    if not indices:
        print('Нет данных в выбранном диапазоне.')
        return

    day_offset = indices[0] % 7

    for i in indices:
        if i % 7 != day_offset:
            continue

        usd += WEEKLY_INVESTMENT
        usd_list.append(usd)

        period_sum = 0.0
        current_date = dfs[reference_token].loc[i, 'date_dt']

        for token, share in allocation.items():
            series = price_lookup[token]
            available_dates = series.index[series.index <= current_date]
            if available_dates.empty:
                last_value = token_state[token]['values'][-1] if token_state[token]['values'] else 0
                token_state[token]['values'].append(last_value)
                continue

            price = float(series.loc[available_dates[-1]])

            amount = (WEEKLY_INVESTMENT * share) / price
            token_state[token]['amount'] += amount
            usd_value = token_state[token]['amount'] * price
            token_state[token]['values'].append(usd_value)
            period_sum += usd_value

        portfolio_values.append(period_sum)
        date_label = dfs[reference_token].loc[i, 'date']
        investment_dates.append(date_label)

        ref_series = price_lookup[lump_token]
        ref_available = ref_series.index[ref_series.index <= current_date]
        if ref_available.empty:
            lump_price = float(ref_series.iloc[0])
        else:
            lump_price = float(ref_series.loc[ref_available[-1]])
        lump_prices.append(lump_price)

    if not investment_dates or not usd_list:
        print('В выбранном диапазоне нет ни одной недели для инвестиций.')
        return

    for token, state in token_state.items():
        if len(state['values']) < len(portfolio_values):
            # если токен появился позже, дублируем последнюю стоимость для графика
            last_value = state['values'][-1] if state['values'] else 0
            missing = len(portfolio_values) - len(state['values'])
            state['values'].extend([last_value] * missing)

    total_invested = usd_list[-1]
    lump_amount = total_invested / lump_prices[0] if lump_prices and lump_prices[0] else 0
    lump_values = [lump_amount * price for price in lump_prices]

    allocation_label = ', '.join(f'{token} {share * 100:.0f}%' for token, share in allocation.items())
    lump_label = f'Разовая покупка {lump_token}'

    build_chart(investment_dates, lump_values, portfolio_values, usd_list, allocation_label, lump_label)

    peak_value = max(portfolio_values)
    peak_index = portfolio_values.index(peak_value)
    peak_date = investment_dates[peak_index]

    print(f'Диапазон анализа: {start_date.date()} — {end_date.date()}')
    print(f'Инвестировано всего: {usd_list[-1]} USD')
    print(f'Максимальная стоимость портфеля: {peak_value:.2f} USD на {peak_date}')
    print(f'Стоимость портфеля в конце: {portfolio_values[-1]:.2f} USD')
    print(f'Линия buy&hold ({lump_token}): максимум {max(lump_values):.2f}, финал {lump_values[-1]:.2f}')

    for token, state in token_state.items():
        print(f'{token}: максимум {max(state["values"]):.2f} USD, финал {state["values"][-1]:.2f} USD')


if __name__ == '__main__':
    main()
