from flask_restful import Resource, reqparse, current_app
from flask import request
# models
from app.models.users import Users
from app.models.stock_basic_info import StockBasicInfo
from app.models.trade_records import TradeRecords
# sqlalchemy 條件、公式
from sqlalchemy.sql import func
from sqlalchemy import and_, or_, not_
# utils
from .utils import google_log_in


class StockBasicInfoApi(Resource):
    def get(self):
        # 讀取前端的資料
        google_token = request.args.get('google_token', type=str)
        # google oauth client ID
        google_oauth_client_id = current_app.config['GOOGLE_OAUTH2_CLIENT_ID']
        # google驗證
        id_info = google_log_in(google_token, google_oauth_client_id)
        # 從table: users get data
        user = Users.query.filter_by(email=id_info['email']).first()
        # 吐出stock_basic_info_id, volume's sum
        user_on_hand = TradeRecords.query.with_entities(TradeRecords.stock_basic_info_id,
                                                        func.sum(TradeRecords.volume).label('sum')) \
            .filter_by(user_id=user.id).group_by(TradeRecords.stock_basic_info_id)\
            .order_by(TradeRecords.created_at.desc()).all()
        inventory_list = []
        total_inventory_cost = 0
        for i in user_on_hand:
            stock_info = {}
            stock = StockBasicInfo.query.get(i[0])
            if i.sum > 0:
                stock_info['stock_symbol'] = stock.stock_symbol
                stock_info['stock_name'] = stock.stock_name.rstrip()
                stock_info['on_hand_volume'] = int(i.sum)
                # 計算成本
                sell_stock_volume_total_price = TradeRecords.query \
                    .filter(TradeRecords.user_id == user.id, TradeRecords.stock_basic_info_id == stock.id) \
                    .with_entities(func.sum(TradeRecords.volume * TradeRecords.cost).label('sum')).first()
                sell_stock_volume_cost_avg = round(float(sell_stock_volume_total_price.sum) / float(i.sum), 2)
                stock_info['cost'] = sell_stock_volume_cost_avg
                # 最近交易日期
                stock_recent_trade = TradeRecords.query\
                    .filter(TradeRecords.user_id == user.id, TradeRecords.stock_basic_info_id == stock.id)\
                    .order_by(TradeRecords.created_at.desc()).first()
                recent_trade_date = stock_recent_trade.created_at
                stock_info['updated_at'] = recent_trade_date.strftime("%Y-%m-%d %H:%M:%S")
                total_inventory_cost += stock_info['on_hand_volume'] * stock_info['cost']
                inventory_list.append(stock_info)
        quick_review_info = {
            'total_cost': 0,
            'total_sell': 0,
            'total_profit': 0,
            'profit_percent': '0%',
        }
        sell_stock_list = TradeRecords.query.filter(TradeRecords.volume < 0,
                                                    TradeRecords.user_id == user.id).all()
        if len(sell_stock_list) > 0:
            for i in sell_stock_list:
                quick_review_info['total_cost'] += round(abs(i.volume * i.cost))
                quick_review_info['total_sell'] += round(abs(i.volume * i.price))
            quick_review_info['total_profit'] = quick_review_info['total_sell'] - quick_review_info['total_cost']
            quick_review_info['profit_percent'] = '{percent:.2%}'\
                .format(percent=(quick_review_info['total_profit'] / quick_review_info['total_cost']))

        return {
            'quick_review_info': quick_review_info,
            'total_inventory_cost': total_inventory_cost,
            'inventory_count': len(inventory_list),
            'inventory_list': inventory_list
        }

    def post(self):
        """
        提供股票資訊
        - 提供股票名稱
        """
        # 讀取前端資料
        json_data = request.json
        """
        - 判斷執行事項:
            - 查詢資料
            - 查詢可賣出股票
            - 提交表單
        """
        if json_data['action'] == 'submit':
            user = Users.query.filter_by(email=json_data['user_email']).first()
            trade_record = TradeRecords(**json_data['form'])
            # 利用relationship去新增Post
            user.create_trade_record(trade_record)
            return "交易成功"
        elif json_data['action'] == 'get_stock_name':
            response = {
                'stock_name': "",
                'stock_basic_info_id': '',
                'sell_stock_volume': 0,
                'cost': 0
            }
            stock = StockBasicInfo.query.filter_by(stock_symbol=json_data['stock_symbol']).first()
            user = Users.query.filter_by(email=json_data['user_email']).first()
            if stock is not None:
                response['stock_name'] = stock.stock_name
                response['stock_basic_info_id'] = stock.id
                # 計算sell_stock_volume_cost_avg
                sell_stock_volume = TradeRecords.query \
                    .filter(TradeRecords.user_id == user.id, TradeRecords.stock_basic_info_id == stock.id) \
                    .with_entities(func.sum(TradeRecords.volume).label('sum')).first()
                if sell_stock_volume.sum:
                    sell_stock_volume_total_price = TradeRecords.query \
                        .filter(TradeRecords.user_id == user.id, TradeRecords.stock_basic_info_id == stock.id) \
                        .with_entities(func.sum(TradeRecords.volume * TradeRecords.cost).label('sum')).first()
                    sell_stock_volume_cost_avg = round(float(sell_stock_volume_total_price.sum) / float(sell_stock_volume.sum), 2)
                    response['sell_stock_volume'] = float(sell_stock_volume.sum)
                    response['cost'] = sell_stock_volume_cost_avg
            return response
        elif json_data['action'] == 'get_stock_symbol_list':
            user = Users.query.filter_by(email=json_data['user_email']).first()
            # 吐出stock_basic_info_id, volume's sum
            user_on_hand = TradeRecords.query.with_entities(TradeRecords.stock_basic_info_id,
                                                            func.sum(TradeRecords.volume).label('sum')) \
                .filter_by(user_id=user.id).group_by(TradeRecords.stock_basic_info_id).all()
            stock_symbol_list = []
            for i in user_on_hand:
                if i.sum > 0:
                    stock = StockBasicInfo.query.get(i.stock_basic_info_id)
                    stock_symbol_list.append(stock.stock_symbol)
            return stock_symbol_list
