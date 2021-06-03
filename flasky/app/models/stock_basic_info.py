from app import db
from .db_abstract import DBAbstract


class StockBasicInfo(DBAbstract):
    """table: 股票基本資訊"""
    __tablename__ = 'stock_basic_info'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(20), nullable=False, unique=True)
    stock_name = db.Column(db.String(60), nullable=False)
    # relationship
    # stock_basic_info: trade_records = one : many
    trade_records = db.relationship('TradeRecords', backref='stock_basic_info', lazy=True)
    # stock_basic_info: stock_data = one : many
    stock_data = db.relationship('StockData', backref='stock_basic_info', lazy=True)
    # stock_basic_info: stock_chip = one : many
    stock_chip = db.relationship('StockChip', backref='stock_basic_info', lazy=True)
    # stock_basic_info:three_days_predict = 1:1
    three_days_predict = db.relationship("ThreeDaysPredict", uselist=False, lazy=True, backref="stock_basic_info")
    # stock_basic_info:five_days_predict = 1:1
    five_days_predict = db.relationship("FiveDaysPredict", uselist=False, lazy=True, backref="stock_basic_info")
