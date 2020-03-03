# stock-analysis
Dashboard to Visualize Stock Data


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
    
    
        
    