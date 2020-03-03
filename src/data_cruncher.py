import pandas as pd
from typing import Optional, Union
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
    def compare_stock_gdp(cls, df_org: pd.DataFrame, ticker: str, *args,
                          **kwargs):
        def _increase_avg(df: pd.DataFrame, window=10):
            _df = df.shift(-1)
            _df = (_df - df) / df
            return _df[-1 * window:].mean()

        logging.info('Waiting for country code...')
        # from data_sniffer import DataSniffer as ds
        # _ticker = ds.info(ticker)
        # country = pycountry.countries.get(name=_ticker['country']).alpha_2
        country = 'US'

        gdp, gdp_id = cls.collect_gdp_data(df_org.index[0], df_org.index[-1],
                                           country)
        _df = cls.stock_data_yearly(df_org)

        _stock = _increase_avg(_df['close'])
        _gdp = _increase_avg(gdp[gdp_id])

        return _stock, _gdp, country


if __name__ == '__main__':
    _ticker = 'msft'
    from data_sniffer import DataSniffer as ds

    _df = ds.download(_ticker)
    print(Cruncher.compare_stock_gdp(_df, _ticker))
