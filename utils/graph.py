import plotly.graph_objects as go


def candlestick_trace(df):
    return go.Candlestick(
        x=df['Date'],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        increasing=dict(line=dict(color="#00ff00")),
        decreasing=dict(line=dict(color="red")),
        showlegend=False,
        name="candlestick",
    )


def line_trace(df):
    trace = go.Scatter(
        x=df['Date'], y=df["Close"], mode="lines", showlegend=False, name="line"
    )
    return trace