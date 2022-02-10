

import cryptowatch as cw
import pandas as pd
from datetime import datetime, timedelta
import json

!pip install --upgrade cryptowatch-sdk

!pip install cryptowatch-SDK

gmee = cw.instruments.get("BONDLYUSDT")._http_response.content
gmee_json = json.loads(gmee)

exchange = "GATEIO"
pairbase = "USDT"



cw.api_key="YMH5J1WLH1HZSA0E09DV"

token_list = ["ETH", "BTC", "SAND", "BONDLY", "REVV"]
tickers = [exchange+":"+i+pairbase for i in token_list]

column_names =['ticker','close_timestamp', 'open', 'high', 'low', 'close', 'volume', 'volume_quote']
token_candle = pd.DataFrame(columns=column_names)

for ticker in tickers: 
    candle = cw.markets.get(ticker, ohlc=True, periods=["1d"])
    #print(candle._http_response.content)
    candles = candle.of_1d[-100:] #get the latest 100 days candles
    for candle in candles:
      candle.insert(0, ticker.split(":")[-1])
      token_candle.loc[len(token_candle)] = candle
    print(ticker)



token_candle["close_timestamp"] = token_candle["close_timestamp"].astype(int)
token_candle["close_timestamp"] = token_candle["close_timestamp"].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%d-%m-%Y'))

token_candle.to_excel("historical token price.xlsx")

