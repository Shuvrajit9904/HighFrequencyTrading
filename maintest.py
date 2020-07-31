#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:48:06 2020

@author: shuvrajit
"""
import datetime
import pandas as pd
import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

import matplotlib.pyplot as plt

my_share = share.Share('NCLH')
symbol_data = None

try:
    symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                          0.03,
                                          share.FREQUENCY_TYPE_MINUTE,
                                          1)
except YahooFinanceError as e:
    print(e.message)
    sys.exit(1)

stocks = ['F', 
          'GE', 
          'AAL', 
          'DIS', 
          'DAL', 
          'AAPL', 
          'MSFT', 
          'TSLA', 
          'CCL', 
          'GPRO', 
          'ACB', 
          'PLUG', 
          'NCLH'  ]

df = pd.DataFrame.from_dict(symbol_data)
df['timestamp'] = df['timestamp'].apply(lambda x : datetime.datetime.fromtimestamp(x / 1e3))
print(df[['timestamp', 'close']])
plt.plot(symbol_data['close'])
plt.ylabel('some numbers')
plt.show()