import argparse
from typing import List
import sql_parser as sp

__parser = argparse.ArgumentParser()
__parser.add_argument("--sql", type=str,
                      required=True, help="SQL used to gather stock data for ticker/s")
__parser.add_argument("--tickers", type=str, nargs='+',
                      required=False, help="ticker/s to track stock data for/ space separated input.")
__parser.add_argument("--graph", type=str, nargs='+',
                      required=False, help="Graph to generate for collected data.")

__TICKERS = ['MSFT', 'GOOGL', "AMZN", 'TSLA', 'BABA', 'AAPL']


class Stocky:
    _columns = ['Open', 'Close', 'High', 'Low', 'Volume']

    def __init__(self, tickers: List[str], sql: str):
        self._tickers = tickers
        self._sql = sql

    def process_sql(self):
        parser = sp.SqlParser(tickers=self._tickers, columns=self._columns, verbose=True)
        parser.parse(self._sql)


if __name__ == '__main__':
    _args = __parser.parse_args()
    _sql = _args.sql

    _tickers = __TICKERS
    if _args.tickers:
        _tickers = _args.tickers

    _stocky = Stocky(_tickers, _sql)
    _stocky.process_sql()
