from moz_sql_parser import parse
from typing import Dict, List, Union
from data_processor import Processor as dp
from data_sniffer import DataSniffer as ds
import operator
import datetime
from utils import utility
import pandas as pd


class SQLParseError(Exception):
    pass


class SqlParser:
    _TICKER = 'tickers'
    _binary_ops = ['lt', 'lte', 'gt', 'gte', 'eq']

    def __init__(self, tickers: List[str], columns: List[str]):
        self._tickers = [tick.lower() for tick in tickers]
        self._columns = [col.lower() for col in columns]

        self._select = []
        self._from = []
        self._ticker = None

    def _visit_bin_op(self, clause: Dict):
        def _raise_sqlerror():
            raise SQLParseError('Invalid <binops> found...')

        def _validate_operand(op):
            if isinstance(op, str):
                if op not in self._select + ['date']:
                    raise SQLParseError(f'<operand>: {op} must be present in <select>... or  use <select> *')
                return op, None
            elif isinstance(op, dict):
                _func, _op = list(op.keys())[0], list(op.values())[0]
                if _func not in dp.data_operations():
                    raise SQLParseError(f'<function>: {_func} not defined over <operand>: {_op}')
                return _op, _func
            else:
                _raise_sqlerror()

        _operand = list(clause.values())[0]
        _operatr = None
        if clause.get('lt'):
            _operatr = operator.lt

        elif clause.get('lte'):
            _operatr = operator.le
        elif clause.get('gt'):
            _operatr = operator.gt
        elif clause.get('gte'):
            _operatr = operator.ge
        elif clause.get('eq'):
            _operatr = operator.eq
        else:
            raise SQLParseError('Invalid operation in <where> clause.')
        _op, _func = _validate_operand(_operand[0])
        return self.execute_query(operatr=_operatr, operand=_op, value=_operand[1], func=_func)

    def _validate_select_clause(self, clause):
        _valid_select = self._columns + ['*']

        def _raise_select_error():
            raise SQLParseError(f'<select> must include valid columns: {_valid_select}')

        if isinstance(clause, str):
            if clause == '*':
                self._select.extend(self._columns)
            elif clause in self._columns:
                self._select.append(clause)
            else:
                _raise_select_error()
        elif isinstance(clause, dict):
            self._validate_select_clause(clause.get('value'))
        else:
            _raise_select_error()

    def _validate_from_clause(self, clause):
        def _raise_from_error():
            raise SQLParseError(f'query only valid on tickers: {self._valid_tables()}')

        if isinstance(clause, str):
            if clause == self._TICKER:
                self._from.extend(self._tickers)
            elif clause in self._valid_tables():
                # self._from.append((clause,))
                self._from.append(clause)
            else:
                _raise_from_error()

        elif isinstance(clause, dict):
            self._validate_from_clause(clause.get('value'))
            # if clause['value'] not in self._valid_tables():
            #     _raise_from_error()
            # self._from.append((clause['value'], clause['name']))
            # self._from.append(clause['value'])
        elif isinstance(clause, list):
            for _clause in clause:
                self._validate_from_clause(_clause)
            _from = [f[0] for f in self._from]
            if self._TICKER in _from:
                raise SQLParseError('<tickers> keyword can not be used with tickers list.')
        else:
            _raise_from_error()

    def _validate_where_clause(self, clause) -> Union[pd.Index, List[pd.Index]]:
        def _raise_where_error():
            raise SQLParseError('Invalid clause <where>')

        if isinstance(clause, dict):
            if clause.get('and'):
                if not isinstance(clause['and'], list):
                    _raise_where_error()
                result_index = self._validate_where_clause(clause['and'])
                return utility.index_intersection(result_index)
            elif clause.get('or'):
                if not isinstance(clause['or'], list):
                    _raise_where_error()
                result_index = self._validate_where_clause(clause['or'])
                return utility.index_union(result_index)
            elif len(clause) == 1 and list(clause.keys())[0] in self._binary_ops:
                return self._visit_bin_op(clause)
            else:
                _raise_where_error()
        elif isinstance(clause, list):
            _result = []
            for _where in clause:
                _result.append(self._validate_where_clause(_where))
            return _result
        else:
            _raise_where_error()

    def _valid_tables(self):
        return self._tickers + [self._TICKER]

    def _validate_stmt(self, sql: Dict):
        if sql['select']:
            self._validate_select_clause(sql['select'])
        else:
            raise SQLParseError('query must include clause <select>...')

        if sql['from']:
            _from = sql['from']
            self._validate_from_clause(_from)
        else:
            raise SQLParseError('query must include clause <from>...')
        if sql['where']:
            for _ticker in self._from:
                self._ticker = _ticker
                print(self._validate_where_clause(sql['where']))

    def parse(self, stmt: str):
        sql = parse(stmt.lower())

        # Validate the statemet
        self._validate_stmt(sql)
        return sql

    def execute_query(self, operatr: operator, operand, value, func):
        if self._ticker is None:
            raise AttributeError('Ticker value not set.')
        if func:
            return dp.execute(self._ticker, operatr, operand, value, func).index
            # print(dp.execute(ticker, operatr, operand, value, func)[self._select])
        else:
            df = ds.download(self._ticker)
            if operand == 'date':
                value = datetime.datetime.fromisoformat(value)
                _df = df.reset_index()
                _df = _df[operatr(_df['date'], value)]
                _df.set_index('date', inplace=True)
                # print(_df)
                return _df.index
            else:
                return df[operatr(df[operand], value)].index
                # print(df[operatr(df[operand], value)][self._select])

    def des(self):
        print(f'select: {self._select}, from: {self._from}')


if __name__ == '__main__':
    _tickers = ['MSFT', 'Googl']
    _columns = ['Open', 'Close', 'High', 'Low', 'Volume']
    _sp = SqlParser(_tickers, _columns)
    # _query = 'select MA(Open) as ma_open from tablename where date between "2019-08-12" and "2020-01-01" and interval="id";'
    _query = 'select * from tickers where  change(open) >= "10%" and date >= "2000-01-25";'
    print(_sp.parse(_query))
    # _sp.des()
