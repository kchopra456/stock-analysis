FROM python:3.7.6-slim

WORKDIR /src

RUN python3 -m pip install yfinance

RUN python3 -m pip install plotly==3.10.0

RUN python3 -m pip install moz_sql_parser

#RUN python3 -m pip install dash==1.0.0
#
#RUN python3 -m pip install gunicorn==19.9.0
#
#RUN python3 -m pip install requests


COPY src /src