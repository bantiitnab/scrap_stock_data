# 1. get all stock names
# 2. get all information about them and save in csv file
# stock_price: price , date

import csv
import pandas as pd
import os
import requests
import json 

class GetStockData:
    def __init__(self):
        self.stocks_code = self.get_stocks_code()

    def get_stocks_code(self): 
        
        basepath = 'data/'
        filename = 'bse100.csv'
        filename = 'nseall.csv'
        filepath = basepath + filename
        print(filepath)

        with open(filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            stocks_code = []
            for row in reader:                
                # stocks_code.append([row['Security Name']])
                stocks_code.append([row['SYMBOL']])
        print(len(stocks_code))
        return stocks_code

    

    def get_data_from_yahoo(self):
        filepath = 'stock_price_yahoo.csv'
        with open(filepath, 'w') as fp:
            fp_writer = csv.writer(fp, delimiter=',', quoting=csv.QUOTE_NONE, quotechar='|')
            fp_writer.writerow(['stock_code', 'Date', 'Open' , 'High', 'Low', 'Close', 'Adj Close', 'Volume'])    
            jar = requests.cookies.RequestsCookieJar()
            jar.set(version=0, name='B', value='ab5qf4dcthd7k&b=3&s=sn', port=None, domain='.yahoo.com', path='/', secure=False, expires=1538910324, discard=False, comment=None, comment_url=None, rest={}, rfc2109=False)
            crumb = 'RKG3rTGMMit'

            for n, stock_code in enumerate(self.stocks_code[:2]):
                print(n, stock_code)            
                CSV_URL = 'https://query1.finance.yahoo.com/v7/finance/download/{}.NS?period1=1167589800&period2=1523867011&interval=1d&events=history&crumb={}'.format(stock_code[0], crumb)
                download = requests.get(CSV_URL, cookies=jar)
                decoded_content = download.content.decode('utf-8')
                cr = csv.reader(decoded_content.splitlines(), delimiter='~')
                
                for (i,row) in enumerate(cr):                             
                    # print(row)           
                    if i == 0: continue
                    row = row[0].split(',')
                    row.insert(0, stock_code[0])
                    fp_writer.writerow(row)
                    
        
        
    def get_data_from_screener(self):
        filepath = 'stock_detail.csv'
        with open(filepath, 'wb') as fp:
            fp_writer = csv.writer(fp, delimiter='~', quoting=csv.QUOTE_NONE, quotechar='|')
            fp_writer.writerow(['stock_code', 'json'])

            for stock_code in self.stocks_code[16:18]:
                print(stock_code)
                r = requests.get('https://www.screener.in/api/company/' + stock_code[0])
                stock_details = r.json()
                fp_writer.writerow([stock_code[0], json.dumps(stock_details)])
                

if __name__ == '__main__':
    stock_data = GetStockData()
    stock_data.get_data_from_yahoo()