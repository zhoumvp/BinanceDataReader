from datetime import datetime
from datetime import timedelta

import CryptoPriceFetch as web

proxies = {'http': 'http://127.0.0.1:7890',
               'https': 'http://127.0.0.1:7890'}
# interval_s
# s -> seconds;
# m -> minutes;
# h -> hours;
# d -> days;
# w -> weeks;
# M -> months

df = web.BinanceDataReader(symbol='BTCUSDT',interval_count=1, interval_s='m',startTime=datetime.now()-timedelta(weeks=1),
                 endTime=datetime.now(),proxies=proxies).read()



