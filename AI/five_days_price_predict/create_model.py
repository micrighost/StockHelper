import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
import pathlib
# database 處理套件
from AI.database.index import *
import pandas as pd
from AI.three_days_price_predict.predict import handle_dataframe


class LstmCreateModel:
    model_folder = '../models/five_days_price_predict/'

    def __init__(self, train_data, model_name):
        self.train_data = train_data
        self.model_name = model_name

    def add_date_data(self):
        """建立日期，訓練要用"""
        self.train_data['Date'] = pd.to_datetime(self.train_data['Date'])
        self.train_data["year"] = self.train_data["Date"].dt.year
        self.train_data["month"] = self.train_data["Date"].dt.month
        self.train_data["date"] = self.train_data["Date"].dt.day
        self.train_data["day"] = self.train_data["Date"].dt.dayofweek + 1
        return self.train_data

    def normalize(self, choice):
        """將所有資料做正規化，而由於timecurrent 是字串非數字，因此先將它drop掉，"""
        # 先刪除Date,這樣才可以正規化(因為Date是文字)
        # self.train_data = self.train_data.drop(["Date"], axis=1)
        open_max = np.max(self.train_data['Open'])
        open_min = np.min(self.train_data['Open'])
        open_mean = np.mean(self.train_data['Open'])
        if choice == 0:  # 逆運算
            self.train_data = self.train_data.apply(lambda x: ((x * (open_max - open_min) + open_mean)))
        if choice == 1:  # 訓練時的加密
            self.train_data = self.train_data.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
        if choice == 2:  # 創造最後預測集時的加密
            self.train_data = self.train_data.apply(lambda x: (x - open_mean) / (open_max - open_min))
        return self.train_data

    def build_train(self, past_day, future_day):
        self.train_data = self.train_data[['Open']]
        x_train = []
        y_train = []
        for i in range(self.train_data.shape[0] - future_day - past_day):
            x_train.append(np.array(self.train_data.iloc[i: i + past_day]))
            y_train.append(np.array(self.train_data.iloc[i + past_day:i + past_day + future_day]["Open"]))
        return np.array(x_train), np.array(y_train)

    @staticmethod
    def split_data(x, y, rate):
        x_train = x[int(x.shape[0] * rate):]
        y_train = y[int(y.shape[0] * rate):]
        x_val = x[:int(x.shape[0] * rate)]
        y_val = y[:int(y.shape[0] * rate)]
        return x_train, y_train, x_val, y_val

    @staticmethod
    def build_many_to_one_model(shape):
        # many to one model
        model = Sequential()
        model.add(LSTM(50, input_length=shape[1], input_dim=shape[2]))
        model.add(Dense(units=32))
        model.add(Dense(units=8))
        # output shape: (1, 1)
        model.add(Dense(1))
        model.compile(loss="mse", optimizer="adam")
        model.summary()
        return model

    def save_model(self, model):
        model_path = pathlib.Path(self.model_folder + self.model_name + '.h5')
        model.save(model_path)


if __name__ == '__main__':
    # 讀取股票資料
    stock = session.query(StockBasicInfo).filter_by(stock_symbol='0050').first()
    stock_data = session.query(StockData).filter_by(stock_basic_info_id=stock.id).\
        order_by(StockData.date.desc()).limit(300)
    # 讀取db_data -> dataframe
    dataframe = pd.read_sql(stock_data.statement, session.bind)
    handle_dataframe = handle_dataframe(dataframe)

    lstm = LstmCreateModel(train_data=handle_dataframe, model_name=stock.stock_symbol)
    # lstm.add_date_data()
    lstm.normalize(choice=1)
    x_train, y_train = lstm.build_train(past_day=5, future_day=1)
    x_train, y_train, x_val, y_val = LstmCreateModel.split_data(x=x_train, y=y_train, rate=0.1)
    # 建模
    trained_model = LstmCreateModel.build_many_to_one_model(x_train.shape)
    # 儲存模型
    lstm.save_model(trained_model)


