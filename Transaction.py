# -*- coding: utf-8 -*-

class Transaction:
    
    def __init__(self, _id, stock_name, timestamp, cost):
        self._id = _id
        self.stock_name = stock_name
        self.timestamp = timestamp
        self.cost = cost