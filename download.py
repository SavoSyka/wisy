import os
from datetime import datetime
from typing import List

from binance import Client
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATE_INPUT_FORMAT = '%d-%m-%Y'


def _env(name: str, *, required: bool = False, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f'Missing required environment variable: {name}')
    return value


def _default_tokens() -> List[str]:
    raw = _env('DEFAULT_TOKENS', default=_env('TOKEN_NAME', default='ADA'))
    return [token.strip().upper() for token in raw.split(',') if token.strip()]


def parse_env_date(name: str, fallback: str) -> datetime:
    raw = _env(name, default=fallback)
    try:
        return datetime.strptime(raw, DATE_INPUT_FORMAT)
    except ValueError as exc:
        raise RuntimeError(
            f'Неверный формат даты в переменной {name}: {raw}. Используйте {DATE_INPUT_FORMAT}'
        ) from exc


def prompt_tokens(default_tokens: List[str]) -> List[str]:
    default_display = ', '.join(default_tokens)
    raw = input(f'Введите токены через запятую ({default_display} по умолчанию): ').strip()
    if not raw:
        return default_tokens
    tokens = [token.replace('/', '').strip().upper() for token in raw.split(',') if token.strip()]
    return tokens or default_tokens


def prompt_date(message: str, default: datetime) -> datetime:
    default_str = default.strftime(DATE_INPUT_FORMAT)
    while True:
        raw = input(f'{message} [{default_str}]: ').strip()
        if not raw:
            return default
        try:
            return datetime.strptime(raw, DATE_INPUT_FORMAT)
        except ValueError:
            print(f'Введите дату в формате {DATE_INPUT_FORMAT}, например {default_str}')


def normalize_pair(token: str, quote_asset: str) -> tuple[str, str]:
    token = token.replace('/', '').strip().upper()
    quote_asset = quote_asset.upper()
    if token.endswith(quote_asset):
        pair = token
        output_name = token[:-len(quote_asset)] or token
    else:
        pair = f'{token}{quote_asset}'
        output_name = token
    return pair, output_name


API_KEY = _env('BINANCE_API_KEY', required=True)
API_SECRET = _env('BINANCE_API_SECRET', required=True)
DEFAULT_TOKENS = _default_tokens()
DEFAULT_START = parse_env_date('DEFAULT_START_DATE', _env('HISTORY_START_DATE', default='21-03-2021'))
DEFAULT_END = parse_env_date('DEFAULT_END_DATE', _env('HISTORY_END_DATE', default='21-03-2024'))
QUOTE_ASSET = _env('QUOTE_ASSET', default='USDT')


def fetch_history(client: Client, pair: str, output_name: str, start: datetime, end: datetime) -> None:
    start_str = start.strftime('%d %b, %Y')
    end_str = end.strftime('%d %b, %Y')
    print(f'Скачиваю {pair} с {start_str} по {end_str}')
    data = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, start_str, end_str)
    if not data:
        print(f' - нет данных для {pair} в заданном диапазоне')
        return

    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', '5', '6', '7', '8', '9', '10', '11'])
    df = df[['date', 'close']]
    df['close'] = df['close'].astype(float)
    df['date'] = pd.to_datetime(df['date'], unit='ms').dt.strftime('%d-%m-%Y')

    os.makedirs('data/xlsx', exist_ok=True)
    os.makedirs('data/csv', exist_ok=True)
    df.to_excel(f'data/xlsx/{output_name}.xlsx', index=False)
    df.to_csv(f'data/csv/{output_name}.csv', index=False)
    print(f' - сохранено в data/xlsx/{output_name}.xlsx и data/csv/{output_name}.csv')


def main() -> None:
    tokens = prompt_tokens(DEFAULT_TOKENS)
    start_date = prompt_date('Введите начальную дату (формат 01-12-2025)', DEFAULT_START)
    end_date = prompt_date('Введите конечную дату (формат 01-12-2025)', DEFAULT_END)
    client = Client(API_KEY, API_SECRET)

    for token in tokens:
        pair, output_name = normalize_pair(token, QUOTE_ASSET)
        fetch_history(client, pair, output_name, start_date, end_date)


if __name__ == '__main__':
    main()
