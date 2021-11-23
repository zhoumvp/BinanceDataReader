import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
from pandas_datareader.base import _BaseReader

BASE_URL  = 'https://api.binance.com/api/v3/klines'

class BinanceDataReader(object):
    def __init__(self,symbol='BTCUSDT',interval='1d',startTime=datetime.now()-timedelta(weeks=4),
                 endTime=datetime.now(),proxies=None):
        self.symbol = symbol
        self.interval = interval
        self.startTime = startTime
        self.endTime = endTime
        self.limit:1000
        self.proxies = proxies

    def read(self):
        columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
                   'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
        df = pd.DataFrame(columns=columns)
        tt = self.startTime
        while tt < self.endTime:
            sTime = tt
            aTime = timedelta(hours=900)
            eTime = tt + aTime
            params = {
                'symbol': self.symbol,
                'interval': self.interval,
                'startTime': round(sTime.timestamp() * 1000),
                'endTime': round(eTime.timestamp() * 1000),
                'limit': 1000
            }

            response = requests.get(BASE_URL, headers={'Accept': 'application/json'},
                                    params=params,
                                    proxies=self.proxies)
            df = df.append(pd.DataFrame(response.json(), columns=columns))
            tt = eTime

        df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
        df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')

        return df

if __name__ == '__main__':
    proxies = {'http': 'http://127.0.0.1:7890',
               'https': 'http://127.0.0.1:7890'}

    # m -> minutes;
    # h -> hours;
    # d -> days;
    # w -> weeks;
    # M -> months

    df = BinanceDataReader(symbol='BTCUSDT',interval='1m',startTime=datetime.now()-timedelta(weeks=1),
                 endTime=datetime.now(),proxies=proxies).read()

    print(df.head())