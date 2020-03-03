import argparse
from typing import List
import sql_parser as sp
from utils import template
from data_cruncher import Cruncher as crunch
import logging

__parser = argparse.ArgumentParser()
__parser.add_argument("--sql", type=str,
                      required=True,
                      help="SQL used to gather stock data for ticker/s")
__parser.add_argument("--tickers", type=str, nargs='+',
                      required=False,
                      help="ticker/s to track stock data for/"
                           " space separated input.")
__parser.add_argument('-v', '--verbose', dest='verbose',
                      action='store_true')

__TICKERS = ['MSFT', 'GOOGL', "AMZN", 'TSLA', 'BABA', 'AAPL']


# logging.basicConfig(level=logging.INFO)

class Stocky:
    _columns = ['Open', 'Close', 'High', 'Low', 'Volume']

    def __init__(self, tickers: List[str], sql: str):
        self._tickers = tickers
        self._sql = sql

    def process_sql(self, verbose):
        parser = sp.SqlParser(tickers=self._tickers,
                              columns=self._columns, verbose=verbose)
        result = parser.parse(self._sql)

        for ticker, data in result.items():
            print(template.query_header.format(ticker))
            if _verbose:
                self._register_filter_output(data[0])
            self._register_last_high(data)
            self._register_gdp_compare(data, ticker)
            print(template.query_footer)

    @classmethod
    def _register_filter_output(cls, df):
        print(template.query_section.format('SQL Result'))
        print(df)

    @classmethod
    def _register_last_high(cls, data, window=10):
        print(template.query_section.format(
            f'Last High Window {window}'))
        _date = crunch.high_window(df_org=data[1], window=window)

    @classmethod
    def _register_gdp_compare(cls, data, ticker):
        print(template.query_section.format(
            f'Compare Stock Rise vs Country GDP growth.'))
        stock, gdp, country = crunch.compare_stock_gdp(df_org=data[1],
                                                       ticker=ticker)

        if stock > gdp:
            print(
                f'Stock growth is faster than {country}\'s GDP:'
                f'\nSTOCK: {stock}\nGDP: {gdp}')
        else:
            print(
                f'Stock growth is slower than {country}\'s GDP:'
                f'\nSTOCK: {stock}\nGDP: {gdp}')


if __name__ == '__main__':
    _args = __parser.parse_args()
    _sql = _args.sql

    _tickers = __TICKERS
    if _args.tickers:
        _tickers = _args.tickers
    _verbose = _args.verbose

    _stocky = Stocky(_tickers, _sql)
    _stocky.process_sql(verbose=_verbose)
