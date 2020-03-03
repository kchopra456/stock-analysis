# Stock-Analysis
Framework to process Stock Data allowing SQL.

##RUN
- Execute `app.py` file with args.
- This modue runs inside docker container, to build the image execute [`build.sh`](build.sh).
- refer [run.sh](run.sh) for docker command to execute module.
 
### command-line parameters
- **--sql**: `required`
    - provide sql query to operate on stock data.
    - [refer](#sql-formatting) for format.
    - example- *... --sql "SELECT * FROM " TICKERS;" ...*
- **--tickers** : `optional`
    - provide ticker/s to collect stock data.
    - example: *... --tickers "MSFT" "GOOGL" ...*
- **--verbose/-v**: `optional`
    - to print query selected table to console.
    - example: *... --verbose ...*

## SQL Formatting
- This module can process `SQL` string to fetch conditional stock data.
- Provide the `SQL` using command-line as `--sql`.

### Details of SQL
- Only `<select>` query is allowed, the format explained below:
```
<SELECT> [{COLUMNS}]
    <FROM> [TICKERS|{TICKERS}]
<WHERE> cond [AND|OR cond...];
```
- COLUMNS:
    - derived form the stock market data.
    - restricted to values: [Open, Close, High, Low, Volume]
    - also allowed `*` symbol to collect all columns from the data.
- TICKERS:
    - refer to the tickers used to track stocks.
    - default values: ['MSFT', 'GOOGL', "AMZN", 'TSLA', 'BABA', 'AAPL']
    - can be changed using `--tickers` commandline arg (_space delimited values_).
- WHERE:
    - provide conditions using operations on columns such as:
        - binary operations ['<', '<=', '>', '>=', '=']
        - ternary operation ['between']
    - operation can be only performed on columns available in the stock data.
    - also allow `data processing` steps to provide better filtering
        - refer [`data_processor.py`](data_processor.py) for details.
#### Examples
- Collect all columns from max period for all tickers.
    - SELECT * FROM TICKERS;
- Collect specific columns from data.
    - SELECT Close, High FROM TICKERS;
- Collect data for specific tickers.
    - SELECT Close FROM MSFT, GOOGL;
- Collect and filter data with basic filtering.
    - SELECT * FROM MSFT, GOOGL WHERE Date between "2020-01-01" AND "2020-02-28";
- Collect and filter data with complex filtering.
    - SELECT * FROM MSFT, GOOGL WHERE Date between "2020-01-01" AND "2020-02-28" and change(open) > "5%";
    - SELECT * FROM MSFT, GOOGL WHERE Date between "2020-01-01" AND "2020-02-28" and change(open) > 10;
    
## References
- https://towardsdatascience.com/a-comprehensive-guide-to-downloading-stock-prices-in-python-2cd93ff821d4
- https://towardsdatascience.com/stock-analysis-in-python-a0054e2c1a4c
- https://medium.com/analytics-vidhya/finance-data-with-python-29e02ce1fae0
- https://research.fb.com/prophet-forecasting-at-scale/
- https://towardsdatascience.com/the-next-level-of-data-visualization-in-python-dd6e99039d5e
- http://www.tylervigen.com/spurious-correlations
- https://www.datacamp.com/community/tutorials/finance-python-trading
- https://plot.ly/python/v3/html-reports/
- https://medium.com/analytics-vidhya/stock-market-trends-b24203484e0f
- https://towardsdatascience.com/python-for-finance-stock-portfolio-analyses-6da4c3e61054
- https://blog.openbridge.com/mode-analytics-the-right-choice-for-you-2984a190e933
- https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
- https://dash-gallery.plotly.host/Portal/