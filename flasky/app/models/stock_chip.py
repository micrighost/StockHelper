from app import db
from .db_abstract import DBAbstract


class StockChip(DBAbstract):
    """table: 三大法人籌碼"""
    __tablename__ = 'stock_chip'
    id = db.Column(db.Integer, primary_key=True)
    stock_basic_info_id = db.Column(db.Integer, db.ForeignKey('stock_basic_info.id'), nullable=False)
    net_buy_volume = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

