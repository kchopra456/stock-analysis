import pandas as pd
from typing import Union, Optional
import operator
from data_sniffer import DataSniffer as ds


class Processor:

    @classmethod
    def data_operations(cls):
        return [cls.change.__name__, cls.increase.__name__, cls.decrease.__name__, cls.moving_average.__name__]

    @classmethod
    def _apply_operation(cls, df: pd.Series, op: operator, value):
        if op == operator.lt:
            return df < value
        if op == operator.le:
            return df <= value
        if op == operator.gt:
            return df > value
        if op == operator.ge:
            return df >= value
        if op == operator.eq:
            return df == value

        raise AttributeError(f'<operator>: {op} not supportted')

    @classmethod
    def _change(cls, df: pd.DataFrame, col: str, ratio: float, absolute: bool = False) -> pd.Series:
        _df = df.shift(-1)
        if ratio is not None:
            _df = (_df[col] - df[col]) / df[col]
        else:
            _df = (_df[col] - df[col])
        if absolute:
            return abs(_df)
        return _df

    @classmethod
    def _define_value(cls, value: float, ratio: float):
        if value is None:
            return ratio
        if ratio is None:
            return value
        raise AttributeError('Expected value/ratio to be not None.')

    @classmethod
    def change(cls, df: pd.DataFrame, col: str, op: operator, value: float = None, ratio: float = None):
        _df = cls._change(df, col, ratio=ratio, absolute=True)
        _value = cls._define_value(value=value, ratio=ratio)
        return _df[op(_df, _value)]
        # return cls._apply_operator(_df, _value, op)

    @classmethod
    def increase(cls, df: pd.DataFrame, col: str, op: operator, value: float = None, ratio: float = None):
        _df = cls._change(df, col, ratio=ratio)
        _df.mask(_df < 0, inplace=True)
        _value = cls._define_value(value=value, ratio=ratio)
        return _df[op(_df, _value)]

    @classmethod
    def decrease(cls, df: pd.DataFrame, col: str, op: operator, value: float = None, ratio: float = None):
        _df = cls._change(df, col, ratio=ratio)
        _df.mask(_df > 0, inplace=True)
        _value = cls._define_value(value=value, ratio=ratio)
        return _df[op(_df, _value)]

    @classmethod
    def moving_average(cls, df: pd.DataFrame, col: str, *args, **kwargs):
        _df = df[col].rolling(window=5).mean()
        return _df

    @classmethod
    def execute(cls, ticker: str, operatr: operator, operand: str, value: Union[int, str, float], func: Optional[str]):
        def _define_value_ratio(input):
            if isinstance(input, int) or isinstance(input, float):
                return input, None
            elif isinstance(input, str):
                if input.endswith('%'):
                    return None, int(input.split('%')[0]) / 100
            else:
                raise ValueError(f'expected value as int/float or percentage value as xx%, but got: {input}')

        value, ratio = _define_value_ratio(value)
        df = ds.download(ticker)
        if func:
            if func == cls.change.__name__:
                return cls.change(df=df, col=operand, op=operatr, value=value, ratio=ratio)
            elif func == cls.increase.__name__:
                return cls.increase(df=df, col=operand, op=operatr, value=value, ratio=ratio)
            elif func == cls.decrease.__name__:
                return cls.decrease(df=df, col=operand, op=operatr, value=value, ratio=ratio)
            elif func == cls.moving_average.__name__:
                return cls.decrease(df=df, col=operand, op=operatr, value=value, ratio=ratio)
            else:
                raise AttributeError(f'function: {func} not defined on class: {cls.__name__}')
