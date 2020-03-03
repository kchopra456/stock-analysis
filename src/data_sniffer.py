import datetime
import yfinance as yf
import pandas as pd

from typing import Union


class SniffingError(Exception):
    pass


class DataSniffer:
    _storage = {}

    @classmethod
    def _collect_cache(cls, ticker: str):
        if cls._storage.get(ticker) is not None:
            return cls._storage[ticker]
        return pd.DataFrame()

    @classmethod
    def _cache_data(cls, ticker: str, df):
        cls._storage.update({ticker: df})

    @classmethod
    def download(cls, ticker: str, start: Union[datetime.datetime, datetime.date] = None, end: Union[datetime.datetime, datetime.date] = None):
        df = cls._collect_cache(ticker)
        if not df.empty:
            return df
        df = yf.download(ticker, start=start, end=end)
        df.reset_index(inplace=True)
        df.columns = [col.lower() for col in df.columns]
        df.set_index('date', inplace=True)
        if df.empty:
            raise SniffingError(f'failed to collect data for ticker: {ticker}')
        cls._cache_data(ticker, df)
        return df

    @classmethod
    def info(cls, ticker: str):
        return yf.Ticker(ticker).info


if __name__ == '__main__':
    _ticker = 'msft'
    df = DataSniffer.download(_ticker).tail(n=5)
    _df = df.shift(-1)
    print((_df - df) / df)
