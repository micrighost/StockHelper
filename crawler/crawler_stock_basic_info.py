from utils import Crawler
import json
from database.index import *  # database 處理套件
import pandas as pd
import time
import random


class CrawlerBasicInfo(Crawler):
    """
    爬蟲: 股票基本資訊
    - stock_basic_info:
        - stock_symbol
        - stock_name
        - industry_type_id
    - stock_basic_info_detail:
        - stock_symbol_id
        - company_address
        - company_phone_number
        - business_description
        - establishment_day
        - TWSE_listed_day
        - OTC_listed_day
    - industry_type
        - id
        - name
    """
    # 存放產業類別
    industry_type_dict = IndustryTypes.get_dict_data()
    # 存放股別類型
    stock_type_dict = StockTypes.get_dict_data()

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
        # 判斷是否要新增industry_type
        self.industry_type_status = ''
        # 判斷是否要新增stock_type
        self.stock_type_status = ''

    def get_data(self, response_text) -> list:
        """抓取資料"""
        json_data = json.loads(response_text)
        print('抓取資料中')
        data = json_data['data']
        print('資料筆數: ', len(data))
        self.data = data
        return self.data

    def data_processing(self):
        """
        資料處理
        - 判別產業類別是否要新增資料
        """
        # 判斷產業類別是否已存在，若不存在加入industry_type。
        if self.data['industryType'] is None:
            self.industry_type_status = None
        elif self.data['industryType'] not in self.industry_type_dict.keys():
            self.industry_type_status = 'create'
            # 字典加入 key 產業類別名稱, value:字典項目數量 + 1
            self.industry_type_dict[self.data['industryType']] = len(self.industry_type_dict) + 1
            print("已加入產業類別字典:{}".format(self.data['industryType']))
        else:
            self.stock_type_status = 'exist'

        # 判斷股票類別是否已存在，若不存在加入stock_type。
        if self.data['stockType'] is None:
            self.stock_type_status = None
        elif self.data['stockType'] not in self.stock_type_dict.keys():
            self.stock_type_status = 'create'
            # 字典加入 key 股票類別名稱, value:字典項目數量 + 1
            self.stock_type_dict[self.data['stockType']] = len(self.stock_type_dict) + 1
            print("已加入股票類別字典:{}".format(self.data['stockType']))
        else:
            self.stock_type_status = 'exist'

    def to_database(self, data):
        """
        資料進入資料庫
        - industry_type
        - stock_basic_info
        - stock_basic_info_detail
        """
        # 判斷industry_type_status
        if self.industry_type_status is None:
            industry_type_id = None
        elif self.industry_type_status == 'create':
            industry_type = IndustryTypes.create(name=self.data['industryType'])
            industry_type_id = industry_type.id
        else:
            industry_type_id = self.industry_type_dict[self.data['industryType']]

        # 判斷stock_type_status
        if self.stock_type_status is None:
            stock_type_id = None
        elif self.stock_type_status == 'create':
            stock_type = StockTypes.create(name=self.data['stockType'])
            stock_type_id = stock_type.id
        else:
            stock_type_id = self.stock_type_dict[self.data['stockType']]

        stock_basic_info = StockBasicInfo.create(stock_symbol=data.stock_symbol,
                                                 stock_name=data.stock_name,
                                                 industry_type_id=industry_type_id,
                                                 stock_type_id=stock_type_id)
        StockBasicInfoDetail.create(stock_symbol=stock_basic_info.stock_symbol,
                                    company_address=self.data['companyAddress'],
                                    company_phone_number=self.data['telephoneNumber'],
                                    business_description=self.data['description'],
                                    establishment_day=self.data['startAtS'])


if __name__ == '__main__':
    headers_raw = '''authority: marketinfo.api.cnyes.com
method: GET
path: /mi/api/v1/TWS:1503:STOCK/info
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
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36
x-cnyes-app: unknown
x-platform: WEB, WEB
x-system-kind: FUND_OLD_DRIVER'''
    # 處理headers
    headers_dict = Crawler.get_dict(str_raw=headers_raw)

    # 讀取csv
    df = pd.read_csv(filepath_or_buffer='./stock_symbol.csv')

    for index, row in df.iterrows():
        print('csv index: {}'.format(index))
        print('股票代號: {}'.format(row.stock_symbol))
        request_url = 'https://marketinfo.api.cnyes.com/mi/api/v1/TWS:' + str(row.stock_symbol) + ':STOCK/info'
        # 創造crawler_basic_info物件
        crawler_basic_info = CrawlerBasicInfo(url=request_url,
                                              headers=headers_dict,
                                              method='get')
        response = crawler_basic_info.request()
        # 拿取資料
        crawler_basic_info.get_data(response_text=response.text)
        # 資料處理: 判斷是否要加入新產業類別
        crawler_basic_info.data_processing()
        # 資料庫存取資料
        crawler_basic_info.to_database(data=row)
        time.sleep(random.randint(5, 10))
        print('=========================')
