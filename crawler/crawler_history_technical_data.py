from utils import Crawler
import json
from database.index import *  # database 處理套件
import pandas as pd
import time
import random
from datetime import datetime


class CrawlerHistoryTechnicalData(Crawler):
    """
    爬蟲: 股票技術指標資料(開盤價、收盤價、最高價、最低價、成交張數)
    """
    def __init__(self, url: str = None, method: str = None, headers: dict = None, **params):
        """
        建構式
        url: 網頁的網址
        headers: 網頁的頭
        **params: 要提供網址的參數
        """
        # crawler 物件
        Crawler.__init__(self, url=url, headers=headers, method=method, **params)
        # 資料存放區
        self.data = None

    def get_data(self, response_text) -> list:
        """抓取資料"""
        json_data = json.loads(response_text)
        print('抓取資料中')
        data = json_data['data']
        print(data)
        print('資料筆數: ', len(data))
        self.data = data
        return self.data

    def data_processing(self):
        """
        資料處理: 每日的資料變成一個字典檔
        [{日期,開盤, 最高, 最低, 收盤, 成交張數}]
        """
        data_length = len(self.data['t'])
        data = []
        for i in range(data_length):
            date = datetime.fromtimestamp(self.data['t'][i]).strftime('%Y-%m-%d')
            opening_price = self.data['o'][i]
            closing_price = self.data['c'][i]
            highest_price = self.data['h'][i]
            lowest_price = self.data['l'][i]
            volume = round(self.data['v'][i])
            date_data = {
                'date': date,
                'opening_price': opening_price,
                'closing_price': closing_price,
                'highest_price': highest_price,
                'lowest_price': lowest_price,
                'volume': volume
            }
            data.append(date_data)
        return data

    @staticmethod
    def to_database(stock_symbol, data):
        """
        資料進入資料庫
        - stock_technical_data
        """
        # 使用股票代號，stock_basic_info query -> object
        stock_basic_info = session.query(StockBasicInfo).filter_by(stock_symbol=stock_symbol).first()
        stock_technical_data = StockTechnicalData(**data)
        # 依靠relationship add stock_technical_data
        stock_basic_info.append_stock_technical_data(stock_technical_data)
        print('股票代號: {}, 日期: {}'.format(stock_basic_info.stock_symbol, data['date']))
        print('已進入資料庫')
        print('========================')


if __name__ == '__main__':
    headers_raw = '''authority: ws.api.cnyes.com
method: GET
path: /ws/api/v1/charting/history?resolution=D&symbol=TWS:2330:STOCK&from=1619325224&to=1585197164
scheme: https
accept: application/json, text/plain, */*
accept-encoding: gzip, deflate, br
accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
origin: https://invest.cnyes.com
referer: https://invest.cnyes.com/
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"
sec-ch-ua-mobile: ?0
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-site
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36
x-cnyes-app: unknown
x-platform: WEB, WEB
x-system-kind: FUND_OLD_DRIVER'''
    # 處理headers
    headers_dict = Crawler.get_dict(str_raw=headers_raw)
    # 日期區間設定(開始日期: 2021-04-26, 結束日期: 2016-01-01)
    start_timestamp = 1619395200  # 起始日期's timestamp
    end_timestamp = 1451606400  # 結束日期's timestamp
    # 讀取csv
    df = pd.read_csv(filepath_or_buffer='./stock_symbol.csv')
    # bug出現在代號2356
    df = df[13309:]
    for index, row in df.iterrows():
        request_symbol = 'TWS:{}:STOCK'.format(row.stock_symbol)  # 進入url的股票代號

        request_url = 'https://ws.api.cnyes.com/ws/api/v1/charting/history?' \
                      'from={}' \
                      '&to={}'.format(start_timestamp, end_timestamp)
        crawler_history_technical_data = CrawlerHistoryTechnicalData(url=request_url,
                                                         headers=headers_dict,
                                                         method='get',
                                                         resolution='D',
                                                         symbol=request_symbol,
                                                         quote=1)
        response = crawler_history_technical_data.request()
        # 拿取資料
        crawler_history_technical_data.get_data(response_text=response.text)
        # 處理資料
        processing_data = crawler_history_technical_data.data_processing()
        # 資料進入資料庫
        for each_date_data in processing_data:
            CrawlerHistoryTechnicalData.to_database(stock_symbol=row.stock_symbol, data=each_date_data)
        time.sleep(random.randint(5, 10))
        print('=========================')
