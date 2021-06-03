import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import pathlib
# database 處理套件
from AI.database.index import *
import pandas as pd


def handle_dataframe(df):
    """預處理dataframe的column。"""
    # yyyy/mm/dd -> year, month, day
    df = df.rename(columns={'date': 'Date', 'opening_price': 'Open', 'closing_price': 'Close',
                            'highest_price': 'High', 'lowest_price': 'Low', 'volume': 'Volume'}, inplace=False)
    df["Date"] = pd.to_datetime(df["Date"])
    df["year"] = df["Date"].dt.year
    df["month"] = df["Date"].dt.month
    df["date"] = df["Date"].dt.day
    df["day"] = df["Date"].dt.dayofweek + 1
    # 轉完後，drop column: date，無法進模型
    # 去除不必要的資料後 -> Open. High, Low, Close, Volume year  month  date  day
    df = df.drop(columns=['Date', 'id', 'stock_basic_info_id'])
    return df


def ai_three_days_predict(df):
    #  用pandas轉成numpy數組
    x = df.values
    # 數據歸一化(最大最小方法)
    min_max_scaler = MinMaxScaler()
    min_max_scaler.fit(x)
    x = min_max_scaler.transform(x)
    # 讀取模型
    model_path = pathlib.Path('../models/three_days_price_predict/DNN_Model_5Probability.h5')  # 模型路徑
    load_model = tf.keras.models.load_model(model_path)  # 載入模型
    # 使用模型預測
    model_output = load_model.predict(x)
    # data: [漲跌幅小於一趴, 漲幅大於一趴小於三趴, 跌幅大於一趴小於三趴, 漲幅大於三趴, 跌幅大於三趴]
    return model_output[-1]  # 回傳model_output最後一筆


if __name__ == '__main__':
    # 讀取資料
    stock = session.query(StockBasicInfo).filter_by(stock_symbol='2892').first()
    stock_data = session.query(StockData).filter_by(stock_basic_info_id=stock.id).\
        order_by(StockData.date)
    # 讀取db_data -> dataframe
    dataframe = pd.read_sql(stock_data.statement, session.bind)
    handle_dataframe = handle_dataframe(dataframe)
    # three_days_predict_output: [漲跌幅小於一趴, 漲幅大於一趴小於三趴, 跌幅大於一趴小於三趴, 漲幅大於三趴, 跌幅大於三趴]
    three_days_predict_output = ai_three_days_predict(handle_dataframe)
    # 整理資料
    three_days_predict_data = {
        'three_days_no_change': round(three_days_predict_output[0], 2),
        'three_days_increase_one_percent': round(three_days_predict_output[1], 2),
        'three_days_decrease_one_percent': round(three_days_predict_output[2], 2),
        'three_days_increase_three_percent': round(three_days_predict_output[3], 2),
        'three_days_decrease_three_percent': round(three_days_predict_output[4], 2)
    }
    # 資料進入資料庫
    three_days_predict = ThreeDaysPredict(**three_days_predict_data)
    stock.append_three_days_predict_data(three_days_predict)
