from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float
)
from sqlalchemy.orm import relationship
from AI.database import Base, session


class FiveDaysPredict(Base):
    """table: 股票預測五天價格"""
    __tablename__ = 'five_days_predict'
    stock_basic_info_id = Column(Integer, ForeignKey('stock_basic_info.id'), primary_key=True)
    future_first_day = Column(Float, nullable=False)
    future_second_day = Column(Float, nullable=False)
    future_third_day = Column(Float, nullable=False)
    future_forth_day = Column(Float, nullable=False)
    future_fifth_day = Column(Float, nullable=False)
    # relationship
    # stock_basic_info:three_days_predict = 1:1
    stock_basic_info = relationship("StockBasicInfo", back_populates="five_days_predict")

    def __init__(self, **data):
        """建構子"""
        for key, item in data.items():
            setattr(self, key, item)

    @classmethod
    def create(cls, **kwargs):
        """新增"""
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj
