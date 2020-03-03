import argparse
from typing import List
import sql_parser as sp
from utils import template
from data_cruncher import Cruncher as crunch
import logging
import os
import datetime
import pandas as pd

__parser = argparse.ArgumentParser()
__parser.add_argument("--sql", type=str,
                      required=True,
                      help="SQL used to gather stock data for ticker/s")
__parser.add_argument("--tickers", type=str, nargs='+',
                      required=False,
                      help="ticker/s to track stock data for/"
                           " space separated input.")
__parser.add_argument("-o", type=str, required=False,
                      help="output directly to unload generated files.")
__parser.add_argument("--data", type=str, required=False, action='append',
                      nargs=4,
                      help="to compare stock value with external data source "
                           "`identifier` `path` `index` `column`")
__parser.add_argument('-v', '--verbose', dest='verbose',
                      action='store_true')

__TICKERS = ['MSFT', 'GOOGL', "AMZN", 'TSLA', 'BABA', 'AAPL']
__output_dir = './.output'


# logging.basicConfig(level=logging.INFO)

class Stocky:
    _columns = ['Open', 'Close', 'High', 'Low', 'Volume']

    def __init__(self, tickers: List[str], sql: str, output_dir: str):
        self._tickers = tickers
        self._sql = sql
        self._outdir = output_dir
        self._ts = datetime.datetime.now()
        self.configure()

    def configure(self):
        if os.path.exists(self._outdir):
            if not os.path.isdir(self._outdir):
                raise AttributeError('path provided for'
                                     ' output must be a directory.')
        else:
            os.mkdir(self._outdir)

    def process_sql(self, verbose, compare_data: List[List[str]]):
        parser = sp.SqlParser(tickers=self._tickers,
                              columns=self._columns, verbose=verbose)
        result = parser.parse(self._sql)

        for ticker, data in result.items():
            print(template.query_header.format(ticker))

            self._register_filter_output(data[0], ticker, _verbose, )
            self._register_last_high(data)
            self._register_gdp_compare(data, ticker)
            for external_spec in compare_data:
                self._register_ext_compare(data, ticker, external_spec)
            print(template.query_footer)

    def _register_filter_output(self, df: pd.DataFrame, ticker, verbose):
        if verbose:
            print(template.query_section.format('SQL Result'))
            print(df)
        _csv_path = f'{self._outdir}/{ticker}-{self._ts}.csv'
        df.to_csv(_csv_path)

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

    @classmethod
    def _register_ext_compare(cls, data, ticker, external_spec):
        print(template.query_section.format(
            f'Compare Stock Rise vs {external_spec[0]}.'))
        stock, ext, identifier = crunch.compare_external_source(df_org=data[1],
                                                                ticker=ticker,
                                                                external_spec=external_spec)

        if stock > ext:
            print(
                f'Stock growth is faster than {identifier}:'
                f'\nSTOCK: {stock}\n{identifier}: {ext}')
        else:
            print(
                f'Stock growth is slower than {identifier}'
                f'\nSTOCK: {stock}\n{identifier}: {ext}')


if __name__ == '__main__':
    _args = __parser.parse_args()
    _sql = _args.sql

    _tickers = __TICKERS
    if _args.tickers:
        _tickers = _args.tickers
    _external_sources = []
    if _args.data:
        _external_sources = _args.data
    _outputdir = __output_dir
    if _args.o:
        _outputdir = _args.o
    _verbose = _args.verbose
    _stocky = Stocky(_tickers, _sql, _outputdir)
    _stocky.process_sql(verbose=_verbose, compare_data=_external_sources)
