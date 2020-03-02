import datetime
import yfinance as yf
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
from utils import graph

tickers = ['MSFT', 'GOOGL', 'TSLA', 'AMZN', 'BABA', 'JNPR']
# tickers = ['MSFT', 'GOOGL']
fdata = dict()
for tick in tickers:
    # _df = yf.download(tick)
    fdata.update({tick: yf.download(tick)})

app = dash.Dash(
    __name__, meta_tags=[{"name": "Stock Analysis", "content": "width=device-width"}],
)

server = app.server

# Create DROP DOWN for tickers.
tickers_options = [
    {"label": tick, "value": tick}
    for tick in tickers
]

app.layout = html.Div(
    children=[html.Div(className="row container-display",
                       children=[
                           html.Div(
                               className="pretty_container four columns",
                               children=[
                                   dcc.Dropdown(
                                       className="div-currency-toggles",
                                       id="ticker-select",
                                       options=tickers_options,
                                       value=tickers_options[0]["value"],
                                       multi=False,
                                   ),
                                   dcc.DatePickerRange(
                                       className="div-currency-toggles",
                                       id='stock-date-picker-range',
                                       min_date_allowed=datetime.date(1950, 1, 1),
                                       max_date_allowed=datetime.date.today(),
                                       # initial_visible_month=datetime.date(2017, 8, 5),
                                       start_date=datetime.date(2020, 1, 1),
                                       end_date=datetime.date.today(),
                                   )
                               ]),
                           html.Div(
                               className="pretty_container",
                               # id='stock-data-candlestick',
                               children=[dcc.Graph(id="stock-data-candlestick")]
                               # style={'max-height': '200px'}
                           ),

                       ]),
              html.Div(className="row container-display",
                       children=[
                           html.Div(
                               className="pretty_container",
                               # id='stock-data-candlestick',
                               children=[dcc.Graph(id="stock-data-linetrace")]
                               # style={'max-height': '200px'}
                           ),

                       ]),
              html.Div(
                  className="pretty_container",
                  id='stock-data-table',
                  style={'max-height': '200px'}
              ),
              ])


@app.callback(output=Output('stock-data-table', 'children'),
              inputs=[Input('ticker-select', 'value'),
                      Input('stock-date-picker-range', 'start_date'),
                      Input('stock-date-picker-range', 'end_date')
                      ])
def show_stock_data_table(ticker, start_date, end_date):
    df = fdata[ticker]
    df = df.reset_index()
    start_date = datetime.datetime.fromisoformat(start_date)
    end_date = datetime.datetime.fromisoformat(end_date)
    df = df[df['Date'].between(start_date, end_date)]
    return [dash_table.DataTable(data=df.to_dict('records'),
                                 columns=[{'name': i, 'id': i} for i in df.columns], page_size=10)]


@app.callback(output=Output('stock-data-candlestick', 'figure'),
              inputs=[Input('ticker-select', 'value'),
                      Input('stock-date-picker-range', 'start_date'),
                      Input('stock-date-picker-range', 'end_date')
                      ])
def show_stock_candlestick(ticker, start_date, end_date):
    df = fdata[ticker]
    df = df.reset_index()
    start_date = datetime.datetime.fromisoformat(start_date)
    end_date = datetime.datetime.fromisoformat(end_date)
    df = df[df['Date'].between(start_date, end_date)]

    data = [graph.candlestick_trace(df)]

    return {'data': data}


@app.callback(output=Output('stock-data-linetrace', 'figure'),
              inputs=[Input('ticker-select', 'value'),
                      Input('stock-date-picker-range', 'start_date'),
                      Input('stock-date-picker-range', 'end_date')
                      ])
def show_stock_linetrace(ticker, start_date, end_date):
    df = fdata[ticker]
    df = df.reset_index()
    start_date = datetime.datetime.fromisoformat(start_date)
    end_date = datetime.datetime.fromisoformat(end_date)
    df = df[df['Date'].between(start_date, end_date)]

    data = [graph.line_trace(df)]

    return {'data': data}


if __name__ == "__main__":
    app.run_server(debug=True, port=9000)
