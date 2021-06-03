from app import db
from .db_abstract import DBAbstract


class ThreeDaysPredict(DBAbstract):
    """table: 股票預測三天後價格"""
    __tablename__ = 'three_days_predict'
    stock_basic_info_id = db.Column(db.Integer, db.ForeignKey('stock_basic_info.id'), primary_key=True)
    three_days_increase_one_percent = db.Column(db.Float, nullable=False)
    three_days_increase_three_percent = db.Column(db.Float, nullable=False)
    three_days_no_change = db.Column(db.Float, nullable=False)
    three_days_decrease_one_percent = db.Column(db.Float, nullable=False)
    three_days_decrease_three_percent = db.Column(db.Float, nullable=False)
