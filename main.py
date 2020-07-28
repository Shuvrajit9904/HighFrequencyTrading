# -*- coding: utf-8 -*-

from BuySale import BuySale

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

buysale = BuySale(10000, stocks)
buysale.buy_sell()