docker run --rm stock-analysis \
 /bin/bash -c 'python3 app.py  --sql "SELECT * FROM MSFT, GOOGL WHERE Date= \"2020-01-02\";" --tickers "MSFT" "GOOGL"'