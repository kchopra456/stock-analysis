import plotly.graph_objects as go
import pandas as pd
import dash_table
from typing import List


def candlestick_trace(df):
    return go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        increasing=dict(line=dict(color="#00ff00")),
        decreasing=dict(line=dict(color="red")),
        showlegend=False,
        name="candlestick",
    )


def line_trace(df: pd.DataFrame, col: str):
    trace = go.Scatter(
        x=df.index, y=df[col], mode="lines", showlegend=False, name="line"
    )
    return trace


def data_table(df: pd.DataFrame):
    return go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[col] for col in df.columns],
                   fill_color='lavender',
                   align='left'))
    ])
