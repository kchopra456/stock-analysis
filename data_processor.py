import pandas as pd
from typing import Union


class Processor:

    @classmethod
    def _apply_operator(cls, df, value, op):
        """

        Parameters
        ----------
        df: pd.Series
        value: Union[int,float]
        op: str

        Returns
        -------

        """

        if op == '<':
            return df[df < value].index
        if op == '<=':
            return df[df <= value].index
        if op == '>':
            return df[df > value].index
        if op == '>=':
            return df[df >= value].index
        if op == '==':
            return df[df == value].index

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
    def change(cls, df: pd.DataFrame, col: str, op: str, value: float = None, ratio: float = None):
        _df = cls._change(df, col, ratio=ratio, absolute=True)
        _value = cls._define_value(value=value, ratio=ratio)
        return cls._apply_operator(_df, _value, op)

    @classmethod
    def increase(cls, df: pd.DataFrame, col: str, op: str, value: float = None, ratio: float = None):
        _df = cls._change(df, col, ratio=ratio)
        _df.mask(_df < 0, inplace=True)
        _value = cls._define_value(value=value, ratio=ratio)
        return cls._apply_operator(_df, _value, op)

    @classmethod
    def decrease(cls, df: pd.DataFrame, col: str, op: str, value: float = None, ratio: float = None):
        _df = cls._change(df, col, ratio=ratio)
        _df.mask(_df > 0, inplace=True)
        _value = cls._define_value(value=value, ratio=ratio)
        return cls._apply_operator(_df, _value, op)
