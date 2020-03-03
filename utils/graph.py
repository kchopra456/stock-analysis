import plotly.graph_objects as go
import pandas as pd

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


def line_trace(df: pd.DataFrame):
    trace = go.Scatter(
        x=df.index, y=df["close"], mode="lines", showlegend=False, name="line"
    )
    return trace