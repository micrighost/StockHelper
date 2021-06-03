import numpy as np
import pandas as pd
import pathlib
import tensorflow as tf
# database 處理套件
from AI.database.index import *
from AI.three_days_price_predict.predict import handle_dataframe
import pandas as pd


def normalize(handled_x, choice, origin_data):
    open_max = np.max(origin_data)
    open_min = np.min(origin_data)
    open_mean = np.mean(origin_data)
    if choice == 0:  # 逆運算
        train_norm = handled_x.apply(lambda x:(x * (open_max - open_min) + open_mean))
    if choice == 1:  # 訓練時的加密
        train_norm = handled_x.apply(lambda x:(x - np.mean(x)) / (np.max(x) - np.min(x)))
    if choice == 2:  # 創造最後預測集時的加密
        train_norm = handled_x.apply(lambda x:(x - open_mean) / (open_max - open_min))
    return train_norm


def calculate_days(handled_model, pred_model, days, origin_data, handled_x):
    output_data = origin_data
    x_input = handled_x
    for i in range(days):
        d = pd.DataFrame(pred_model)
        d = normalize(d, 0, origin_data)
        output_data = np.append(output_data, d)
        x_input = np.append(x_input, pred_model)
        x_input = pd.DataFrame(x_input)
        x_input = x_input.iloc[len(x_input) - 5:]
        x_input = x_input.values
        x_input = x_input.reshape((1, 5, 1))
        pred_model = handled_model.predict(x_input)
    return output_data


def handle_data(raw_data):
    raw_data = pd.DataFrame(raw_data)
    raw_data = raw_data.iloc[len(raw_data) - 5:][0]
    output_data = raw_data.values.tolist()
    for i, element in enumerate(output_data):
        output_data[i] = round(element, 2)
    return output_data


if __name__ == '__main__':
    # 讀取資料from db
    stock = session.query(StockBasicInfo).filter_by(stock_symbol='0050').first()
    stock_data = session.query(StockData).filter_by(stock_basic_info_id=stock.id).\
        order_by(StockData.date.desc()).limit(30)
    # 讀取db_data -> dataframe
    dataframe = pd.read_sql(stock_data.statement, session.bind)
    handle_dataframe = handle_dataframe(dataframe)

    train_data_opening_price = handle_dataframe['Open']
    # 整理x
    x = train_data_opening_price.iloc[len(train_data_opening_price) - 5:]
    x = pd.DataFrame(x)
    # 利用訓練時的原始值進行正規化
    x = normalize(x, 2, train_data_opening_price)
    # pandas to numpy
    x = x.values
    # 整形
    x = x.reshape((1, 5, 1))
    # 導入模型
    model_path = pathlib.Path('../models/five_days_price_predict/' + stock.stock_symbol + '.h5')
    model = tf.keras.models.load_model(model_path)
    model_predict = model.predict(x)

    # 計算五天
    data = calculate_days(handled_model=model,
                          pred_model=model_predict,
                          days=5,
                          origin_data=train_data_opening_price,
                          handled_x=x)

    handled_data = handle_data(raw_data=data)
    handled_data = {
        'future_first_day': handled_data[0],
        'future_second_day': handled_data[1],
        'future_third_day': handled_data[2],
        'future_forth_day': handled_data[3],
        'future_fifth_day': handled_data[4],
    }

    print(handled_data)
    five_days_predict = FiveDaysPredict(**handled_data)
    stock.append_five_days_predict_data(five_days_predict)
