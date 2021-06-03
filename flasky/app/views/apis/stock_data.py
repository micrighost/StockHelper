from flask_restful import Resource, reqparse, current_app
from flask import request
# models
from app.models.stock_basic_info import StockBasicInfo
from app.models.stock_data import StockData
from app.models.stock_chip import StockChip
# others
from datetime import datetime


class StockDataApi(Resource):
    def get(self):
        # 預設資料
        response = {
            'latest_info': {
                'date': '',
                'opening_price': '',
                'closing_price': '',
                'highest_price': '',
                'lowest_price': '',
                'volume': '',
                'percent': ''
            },
            'stock_data': {
                'stock_name': '',
                'data_list': ''
            },
            'stock_chip_data': {
                'date_list': '',
                'data_list': ''
            }
        }
        # 讀取前端資料
        stock_symbol = request.args.get('stock_symbol', type=str)
        # 整理K線圖資料
        stock = StockBasicInfo.query.filter_by(stock_symbol=stock_symbol).first()
        if stock is None:
            return None
        stock_data = StockData.query.filter_by(stock_basic_info_id=stock.id).order_by(StockData.date).all()
        stock_data_list = []
        for i in stock_data:
            data = [
                int(i.date.strftime("%s")) * 1000 + 28800000,  # 時差8小時
                i.opening_price,
                i.highest_price,
                i.lowest_price,
                i.closing_price,
                i.volume
            ]
            stock_data_list.append(data)
        response['stock_data']['stock_name'] = stock.stock_name.rstrip()
        response['stock_data']['data_list'] = stock_data_list
        # latest_info
        # 抓出兩筆資料，0: latest, 1: second
        latest_stock_data = StockData.query.filter_by(stock_basic_info_id=stock.id)\
            .order_by(StockData.date.desc()).limit(2).all()
        response['latest_info']['date'] = latest_stock_data[0].date.strftime("%Y-%m-%d")
        response['latest_info']['volume'] = int(latest_stock_data[0].volume)
        response['latest_info']['opening_price'] = latest_stock_data[0].opening_price
        response['latest_info']['closing_price'] = latest_stock_data[0].closing_price
        response['latest_info']['highest_price'] = latest_stock_data[0].highest_price
        response['latest_info']['lowest_price'] = latest_stock_data[0].lowest_price
        percent = (latest_stock_data[0].closing_price - latest_stock_data[1].closing_price) / latest_stock_data[1].closing_price
        response['latest_info']['percent'] = "{0:.2%}".format(percent)
        # stock_chip_data
        latest_thirty_days_stock_chip = StockChip.query.filter_by(stock_basic_info_id=stock.id)\
            .order_by(StockChip.date.desc()).limit(30).all()
        # 排序從過去到現在
        latest_thirty_days_stock_chip.reverse()
        date_list = []
        data_list = []
        for i in latest_thirty_days_stock_chip:
            date_list.append(i.date.strftime("%Y-%m-%d"))
            data_list.append(i.net_buy_volume)
        response['stock_chip_data']['date_list'] = date_list
        response['stock_chip_data']['data_list'] = data_list
        return response
