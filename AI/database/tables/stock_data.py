from sqlalchemy import Column, String, ForeignKey, Date, Float, Integer
from sqlalchemy.orm import relationship
from AI.database import Base, session


class StockData(Base):
    """table: 股票技術指標資訊"""
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True)
    stock_basic_info_id = Column(Integer, ForeignKey('stock_basic_info.id'), nullable=False)
    opening_price = Column(Float, nullable=False)
    closing_price = Column(Float, nullable=False)
    highest_price = Column(Float, nullable=False)
    lowest_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)