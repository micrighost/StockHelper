from utils import Crawler
import json
import pandas as pd


class CrawlerStockSymbol(Crawler):
    """
    爬蟲: 股票代碼、股票名稱
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
        # 存放資料區
        self.data = []

    def get_data(self, response_text) -> list:
        """抓取資料"""
        json_data = json.loads(response_text)
        print('抓取資料日期: ', self.params['date'])
        if json_data['stat'] == "OK":
            data = json_data['data']
            print('資料筆數: ', len(data))
            for each_data in data:
                individual_stock = {}  # 個股的資料存放區
                stock_symbol = each_data[0]  # stock symbol: 股票代號
                stock_name = each_data[1]
                individual_stock['stock_symbol'] = str(stock_symbol)
                individual_stock['stock_name'] = stock_name
                self.data.append(individual_stock)
            return self.data
        else:
            print('打API，未獲取資料。')
            self.data = None

    def data_processing(self):
        """
        資料處理: 把資料處理成dataframe
        """
        stock_symbol_list = []
        stock_name_list = []
        for each_data in self.data:
            stock_symbol_list.append(each_data['stock_symbol'])
            stock_name_list.append(each_data['stock_name'])
        handled_dict = {
            "stock_symbol": stock_symbol_list,
            "stock_name": stock_name_list
        }
        # dataframe
        dataframe = pd.DataFrame(handled_dict)

        return dataframe

    @staticmethod
    def to_csv(dataframe, filename):
        """轉成CSV"""
        dataframe.to_csv(filename, index=False, encoding='utf-8-sig')
        print('資料匯出成功: {}'.format(filename))

    def main(self):
        """
        主程式:
        - request，狀態200，繼續執行。
        - get_data
        - data_processing
        - to csv
        """
        response = Crawler.request(self)
        # 判斷網頁狀態，200(正常才繼續運作)
        if response.status_code == 200:
            # 抓取資料
            self.get_data(response_text=response.text)
            if self.data is not None:
                # 資料處理成dataframe
                dataframe = self.data_processing()
                # 轉出csv
                CrawlerStockSymbol.to_csv(dataframe=dataframe,
                                          filename='stock_symbol.csv')

        else:
            print("沒資料: ", self.params['date'])
        return self.data


if __name__ == '__main__':
    headers_raw = '''Referer: https://realpython.com/
sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'''

    headers_dict = Crawler.get_headers(headers_raw=headers_raw)

# 使用多線程，用日期每天去爬。
    crawler_stock_symbol = CrawlerStockSymbol(url='https://www.twse.com.tw/fund/T86',
                                              headers=headers_dict,
                                              method='get',
                                              response='json',
                                              date='20210415',
                                              selectType='ALL')
    crawler_stock_symbol.main()




