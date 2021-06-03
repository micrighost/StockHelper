from utils import Crawler
import json
from database.index import *  # database 處理套件
import pandas as pd
import time
import random


class CrawlerStockChip(Crawler):
    """
    爬蟲: 股票籌碼資訊
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
        self.data = []

    def get_data(self, response_text) -> list:
        """抓取資料"""
        json_data = json.loads(response_text)
        print('抓取資料中')
        data = json_data['data']
        print('資料筆數: ', len(data))
        self.data = data
        return self.data

    def data_processing(self):
        f"""
        資料處理
        - dict: stock_symbol, net_buy_volume, date
        """
        handled_data = []
        for i in self.data:
            print(i)
            print(i['code'])
            data = {
                'stock_symbol': i['code'],
                'date': i['date'],
                'net_buy_volume': i['totalNetBuySellVolume']
            }
            handled_data.append(data)
        return handled_data

    @staticmethod
    def to_database(data):
        """
        資料進入資料庫
        - stock_chip
        """
        # 判斷industry_type_status
        for i in handled_data:
            StockChip.create(**i)


if __name__ == '__main__':
    headers_raw = '''authority: marketinfo.api.cnyes.com
method: GET
path: /mi/api/v1/investors/buysell/TWS%3A0050%3ASTOCK?from=1621296000&to=1617235200
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
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36
x-cnyes-app: unknown
x-platform: WEB, WEB
x-system-kind: FUND_OLD_DRIVER'''
    # 處理headers
    headers_dict = Crawler.get_dict(str_raw=headers_raw)
    stock_symbol = "0050"
    start_timestamp = '1619222400'  # 2021/4/23
    end_timestamp = '1616457600'  # 2021/3/23
    request_url = 'https://marketinfo.api.cnyes.com/mi/api/v1/investors/buysell/TWS%3A' + stock_symbol + '%3ASTOCK?' \
                  + 'from=' + start_timestamp + '&' + 'to=' + end_timestamp

    # 創造CrawlerStockChip物件
    crawler_stock_chip = CrawlerStockChip(url=request_url,
                                          headers=headers_dict,
                                          method='get')
    response = crawler_stock_chip.request()
    # 拿取資料
    crawler_stock_chip.get_data(response_text=response.text)
    # 資料處理
    handled_data = crawler_stock_chip.data_processing()
    # 資料庫存取資料
    crawler_stock_chip.to_database(data=handled_data)
