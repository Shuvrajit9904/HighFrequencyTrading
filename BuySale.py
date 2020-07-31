import pandas as pd
import time
import sys
import uuid

from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

import matplotlib.pyplot as plt

from Transaction import Transaction


class BuySale:
    
    def __init__(self, balance, stocks):
        self.balance = balance
        self.stocks = stocks
        self.transaction_directory = {}
        self.delete_transactions = []
        self.money_in_market = 0
        
    def get_historical(self, stock_name):
        my_share = share.Share(stock_name)
        symbol_data = None
        
        try:
            symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                                  0.01,
                                                  share.FREQUENCY_TYPE_MINUTE,
                                                  1)            
        except YahooFinanceError as e:
            print(e.message)
            sys.exit(1)
            
        return pd.DataFrame.from_dict(symbol_data)
    
    def should_sell_stock(self, current_price : float, cost:float, tolerance : float, gain : float, stock_name: str) -> bool:
        
        lower_limit = (100 - tolerance) * cost / 100
        upper_limit = (100 + gain) * cost / 100                
        
        if(current_price < lower_limit or current_price > upper_limit):
            return True

        if(current_price > cost):
            return True
        
#        if(current_price < cost and self.should_buy_stock(stock_name) == False):
#            return True

        return False
    
    def sell_stock(self, transaction : Transaction) -> None:
        tolerance = 5
        gain = 2
        current_price = self.get_historical(transaction.stock_name).close.iloc[-1]
        
        if(self.should_sell_stock(current_price, transaction.cost, tolerance, gain, transaction.stock_name)):
            self.balance += current_price
            self.delete_transactions.append(transaction._id)
            print("Sold: {}, Price: {}, Profit/Loss: {}".format(transaction.stock_name, current_price, current_price-transaction.cost))
        else:
            self.money_in_market += current_price
            
    def should_buy_stock(self, stock_name : str ) -> bool:
        # TODO: Implement logic to buy
        series = self.get_historical(stock_name)
                
        return self.slope_sampling(series, 20)
    
    def slope_sampling(self, stock_prices, num_sampling_points):
        count = 0
        
        for _ in range(num_sampling_points):
            df_two_points = stock_prices.sample(2);
            if((df_two_points.timestamp.iloc[0] < df_two_points.timestamp.iloc[-1]) 
            and (df_two_points.close.iloc[0] < df_two_points.close.iloc[-1])):
                count += 1
            elif((df_two_points.timestamp.iloc[0] > df_two_points.timestamp.iloc[-1]) 
            and (df_two_points.close.iloc[0] > df_two_points.close.iloc[-1])):
                count += 1
        if (count > 0.65 * num_sampling_points ):
#            plt.plot(stock_prices['close'])
#            plt.ylabel('some numbers')
#            plt.show()
#            plt.close()
            return True
        
        return False
    
    def buy_stock(self, stock_name: str) -> None:
        stock_details = self.get_historical(stock_name)
        current_price = stock_details.close.iloc[-1]
        if(self.should_buy_stock(stock_name) & (self.balance > current_price)):
            _id = str(uuid.uuid4())
            transaction = Transaction(_id, stock_name, stock_details.timestamp.tail(1), current_price)
            self.transaction_directory[_id] = transaction
            self.balance -= current_price
            print("Purchase: {}, Price: {}".format(stock_name, current_price))
            
    def buy_sell(self):
        while True:
            self.delete_transactions = []
            self.money_in_market = 0            
#            starting_price = self.balance
            for stock in self.stocks:
                self.buy_stock(stock)
            
            print("Remaining Balance: ", self.balance)
            time.sleep(60)
            
            for _id, transaction in self.transaction_directory.items():
                self.sell_stock(transaction)
            
            for _id in self.delete_transactions:
                del self.transaction_directory[_id]

            print("Total Liquid: ", self.balance + self.money_in_market )
            print("Net Gain/Loss in this iteration: ", self.balance + self.money_in_market - 10000)
            print("Balance after this iteration: ", self.balance)
            
    
    
