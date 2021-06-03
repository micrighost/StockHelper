import requests


class Crawler:
    """
    爬蟲(基底類別)
    """
    # 建構式
    def __init__(self, url: str, method: str, headers: dict, **params):
        """
        建構式
        url: 網頁的網址
        headers: 網頁的頭
        **params: 要提供網址的參數
        """
        self.url = url
        self.headers = headers
        self.method = method
        self.params = params

    # instance method
    def request(self):
        """
        發出request
        """
        response = requests.request(method=self.method,
                                    url=self.url,
                                    headers=self.headers,
                                    params=self.params)
        return response

    @staticmethod
    def get_dict(str_raw):
        """
        處理字串變成字典檔
        主要處理網頁的headers跟params。
        """
        handled_dict = {}
        if str_raw is None:
            return handled_dict
        for row in str_raw.split("\n"):
            handled_dict[row.split(': ')[0]] = row.split(': ')[1]
        return handled_dict

    @staticmethod
    def splice_dataframe(dataframe: object, splice: int, part: int):
        """
        切割dataframe
        splice: 切成幾等分
        part: 你要哪一份
        """
        total_rows = dataframe.shape[0]
        # 四捨五入
        splice_rows = round(total_rows / splice)
        df_start_index = (part - 1) * splice_rows
        df_end_index = part * splice_rows
        splice_df = dataframe[df_start_index:df_end_index]
        return splice_df
