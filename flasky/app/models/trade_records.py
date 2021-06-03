from app import db
from .db_abstract import DBAbstract
from datetime import datetime


class TradeRecords(DBAbstract):
    """table: 股票交易紀錄"""
    __tablename__ = 'trade_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stock_basic_info_id = db.Column(db.Integer, db.ForeignKey('stock_basic_info.id'), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return '<TradeRecords: %r>' % self.id
