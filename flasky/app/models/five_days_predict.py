from app import db
from .db_abstract import DBAbstract


class FiveDaysPredict(DBAbstract):
    """table: 股票預測五天價格"""
    __tablename__ = 'five_days_predict'
    stock_basic_info_id = db.Column(db.Integer, db.ForeignKey('stock_basic_info.id'), primary_key=True)
    future_first_day = db.Column(db.Float, nullable=False)
    future_second_day = db.Column(db.Float, nullable=False)
    future_third_day = db.Column(db.Float, nullable=False)
    future_forth_day = db.Column(db.Float, nullable=False)
    future_fifth_day = db.Column(db.Float, nullable=False)
