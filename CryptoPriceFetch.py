import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
from pandas_datareader.base import _BaseReader

BASE_URL  = 'https://api.binance.com/api/v3/klines'

class BinanceDataReader(object):
    def __init__(self,symbol='BTCUSDT',interval_count=1,interval_s='d',startTime=datetime.now()-timedelta(weeks=4),
                 endTime=datetime.now(),proxies=None):
        self.symbol = symbol
        self.interval_count = interval_count
        self.interval_s = interval_s
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
            interval = '%d%s'%(self.interval_count,self.interval_s)
            sTime = tt
            if self.interval_s == 'm':
                aTime = timedelta(minutes=999)
            elif self.interval_s == 'h':
                aTime = timedelta(hours=999)
            elif self.interval_s == 'd':
                aTime = timedelta(days=999)
            elif self.interval_s == 'w':
                aTime = timedelta(weeks=999)
            elif self.interval_s == 'M':
                aTime = timedelta(weeks=999*4)
            elif self.interval_s == 's':
                aTime = timedelta(seconds=999)
            else:
                raise EOFError
            if tt + aTime < self.endTime:
                eTime = tt + aTime
            else:
                eTime = self.endTime
            params = {
                'symbol': self.symbol,
                'interval': interval,
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
        df = df.reset_index(drop=True)
        return df

if __name__ == '__main__':
    proxies = {'http': 'http://127.0.0.1:7890',
               'https': 'http://127.0.0.1:7890'}
    # s -> seconds;
    # m -> minutes;
    # h -> hours;
    # d -> days;
    # w -> weeks;
    # M -> months

    df = BinanceDataReader(symbol='BTCUSDT', interval_count=1, interval_s='m',
                               startTime=datetime.now() - timedelta(weeks=1),
                               endTime=datetime.now(), proxies=proxies).read()

    print(df.head())