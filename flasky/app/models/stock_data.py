from app import db
from .db_abstract import DBAbstract


class StockData(DBAbstract):
    """table: 股票每日數據"""
    __tablename__ = 'stock_data'
    id = db.Column(db.Integer, primary_key=True)
    stock_basic_info_id = db.Column(db.Integer, db.ForeignKey('stock_basic_info.id'), nullable=False)
    opening_price = db.Column(db.Float, nullable=False)
    closing_price = db.Column(db.Float, nullable=False)
    highest_price = db.Column(db.Float, nullable=False)
    lowest_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

