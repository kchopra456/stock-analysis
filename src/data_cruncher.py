import pandas as pd
from typing import Optional, Union, List
import datetime
import pycountry
import logging


# logger = logging.getLogger(__name__)


class Cruncher:

    @staticmethod
    def high_window(df_org: pd.DataFrame, window: int = 10, *args, **kwargs):
        _df = df_org[
            df_org.rolling(window=10).max()['close'] == df_org['close']]
        _value = _df['close'][-1]
        if _df.index[-1] == datetime.datetime.today():
            print(f'Alert! Highest value in last {window} day window: {_value}')
        else:
            print(f'High value in last recorded on {_df.index[-1]}: {_value}')
        return _df.index[-1]

    @classmethod
    def stock_data_yearly(cls, df: pd.DataFrame):
        # Collect Data annually.
        _df = df.resample('A').mean()
        _df.index = pd.to_datetime(_df.index).year

        return _df

    @classmethod
    def collect_gdp_data(cls, start: Union[datetime.datetime, datetime.date],
                         end: Union[datetime.datetime, datetime.date],
                         country: str = 'US'):
        from pandas_datareader import wb
        id = 'NY.GDP.MKTP.CD'

        gdp: pd.DataFrame = wb.download(indicator=id, country=[country],
                                        start=start.year,
                                        end=end.year)
        gdp = gdp.reindex(index=gdp.index[::-1]).reset_index().drop(
            labels='country', axis=1)
        gdp['year'] = pd.to_datetime(gdp['year']).dt.year
        gdp.set_index('year', inplace=True)

        return gdp, id

    @classmethod
    def _increase_avg(cls, df: pd.DataFrame, window=10):
        _df = df.shift(-1)
        _df = (_df - df) / df
        return _df[-1 * window:].mean()

    @classmethod
    def compare_stock_gdp(cls, df_org: pd.DataFrame, ticker: str, *args,
                          **kwargs):

        logging.info('Waiting for country code...')
        # from data_sniffer import DataSniffer as ds
        # _ticker = ds.info(ticker)
        # country = pycountry.countries.get(name=_ticker['country']).alpha_2
        country = 'US'

        gdp, gdp_id = cls.collect_gdp_data(df_org.index[0], df_org.index[-1],
                                           country)
        _df = cls.stock_data_yearly(df_org)

        _stock = cls._increase_avg(_df['close'])
        _gdp = cls._increase_avg(gdp[gdp_id])

        return _stock, _gdp, country

    @classmethod
    def check_annual_index(cls, df: pd.DataFrame):
        _name = df.index.name
        df = df.reset_index()
        _df = df[_name].shift(1)
        _df = (df[_name] - _df)[1:]
        if ((_df == datetime.timedelta(days=365)) | (
                _df == datetime.timedelta(days=366))).all():
            return True
        return False

    @classmethod
    def compare_external_source(cls, df_org: pd.DataFrame, ticker: str,
                                external_spec: List[List[str]], *args,
                                **kwargs):
        try:
            ex_df = pd.read_csv(external_spec[1], index_col=external_spec[2],
                                parse_dates=True)
        except ValueError:
            raise ImportError(
                f'external source load missing columns: {external_spec[2]}')
        if not ex_df.index.is_monotonic:
            raise ImportError('<Dataframe> index must be monotonic increase.')
        if ex_df.index.is_monotonic_decreasing:
            ex_df.index = ex_df.reindex(index=ex_df.index[::-1])

        if cls.check_annual_index(ex_df):
            df_org = cls.stock_data_yearly(df_org)

        _stock = cls._increase_avg(df_org['close'])
        try:
            _external = cls._increase_avg(ex_df[external_spec[3]])
        except KeyError:
            raise ImportError(
                f'External file import do not include column: {external_spec[3]}')

        return _stock, _external, external_spec[0]


if __name__ == '__main__':
    _ticker = 'msft'
    from data_sniffer import DataSniffer as ds

    _df = ds.download(_ticker)
    print(Cruncher.compare_stock_gdp(_df, _ticker))
