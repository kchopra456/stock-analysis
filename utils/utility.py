import pandas as pd
from typing import List


def index_intersection(dfs: List[pd.Index]):
    _df: pd.Index = dfs[0]
    for df in dfs[1:]:
        _df = _df.intersection(df)
    return _df


def index_union(dfs: List[pd.Index]):
    _df: pd.Index = dfs[0]
    for df in dfs[1:]:
        _df = _df.union(df)
    return _df
