from flask_restful import Resource, reqparse, current_app
from flask import request
# models
from app.models.users import Users
from app.models.stock_basic_info import StockBasicInfo
from app.models.trade_records import TradeRecords
from app.models.stock_data import StockData
from app.models.three_days_predict import ThreeDaysPredict
# sqlalchemy 條件、公式
from sqlalchemy.sql import func
from sqlalchemy import and_, or_, not_
import pandas
from datetime import timedelta


class AIPredict(Resource):
    def get(self):
        response = {
            'latest_date': None,
            'stock_name': None,
            'bar_chart_data': None,
            'line_chart_data': None,
            'ai_predict_data': {
            }
        }
        # 讀取前端資料
        stock_symbol = request.args.get('stock_symbol', type=str)
        stock = StockBasicInfo.query.filter_by(stock_symbol=stock_symbol).first()
        # 股票名字
        response['stock_name'] = stock.stock_name.rstrip()
        # 三天預測價格
        stock_three_days_predict = stock.three_days_predict
        three_days_predict = {
            'three_days_increase_one_percent': stock_three_days_predict.three_days_increase_one_percent,
            'three_days_increase_three_percent': stock_three_days_predict.three_days_increase_three_percent,
            'three_days_no_change': stock_three_days_predict.three_days_no_change,
            'three_days_decrease_one_percent': stock_three_days_predict.three_days_decrease_one_percent,
            'three_days_decrease_three_percent': stock_three_days_predict.three_days_decrease_three_percent
        }
        # AI智能預測's data
        ai_three_days_predict = {}
        for key, item in three_days_predict.items():
            ai_three_days_predict[key] = "{0:.1%}".format(item)
        response['ai_predict_data']['three_days_predict'] = ai_three_days_predict

        # bar_chart_data
        response['bar_chart_data'] = three_days_predict

        # 五天預測價格
        stock_five_days_predict = stock.five_days_predict
        stock_five_days_predict_list = [
            stock_five_days_predict.future_first_day,
            stock_five_days_predict.future_second_day,
            stock_five_days_predict.future_third_day,
            stock_five_days_predict.future_forth_day,
            stock_five_days_predict.future_fifth_day
        ]
        # 抓出近30天股票資料
        line_chart_data = []
        stock_data = StockData.query.filter_by(stock_basic_info_id=stock.id).order_by(StockData.date.desc()).first()
        data = [
            int(stock_data.date.strftime("%s")) * 1000,
            stock_data.opening_price
        ]
        line_chart_data.append(data)
        # 最新的交易日
        latest_stock_date = stock_data.date
        response['latest_date'] = latest_stock_date.strftime("%Y-%m-%d")
        # 處理五天預測價格的資料加入日期
        stock_date = latest_stock_date
        for i, element in enumerate(stock_five_days_predict_list):
            stock_date += timedelta(days=1)
            # 日期不能為六、日
            while stock_date.weekday() == 5 or stock_date.weekday() == 6:
                stock_date += timedelta(days=1)
            time_stamp = int(stock_date.strftime("%s")) * 1000
            data = [time_stamp, element]
            line_chart_data.append(data)
        response['line_chart_data'] = line_chart_data
        # AI智能預測's data
        response['ai_predict_data']['five_days_predict'] = stock_five_days_predict_list
        return response



    def post(self):

        return "123"

    # 'three_days_increase_one_percent': "{0:.1%}".format(stock_three_days_predict.three_days_increase_one_percent),
    # 'three_days_increase_three_percent': "{0:.1%}".format(stock_three_days_predict.three_days_increase_three_percent),
    # 'three_days_no_change': "{0:.1%}".format(stock_three_days_predict.three_days_no_change),
    # 'three_days_decrease_one_percent': "{0:.1%}".format(stock_three_days_predict.three_days_decrease_one_percent),
    # 'three_days_decrease_three_percent': "{0:.1%}".format(stock_three_days_predict.three_days_decrease_three_percent)


