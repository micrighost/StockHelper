from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.orm import relationship
from AI.database import Base, session


class StockBasicInfo(Base):
    """table: 股票基本資訊"""
    __tablename__ = 'stock_basic_info'
    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String(20), nullable=False, unique=True)
    stock_name = Column(String(length=45), nullable=False)
    # relationship
    # stock_basic_info:three_days_predict = 1:1
    three_days_predict = relationship("ThreeDaysPredict", back_populates="stock_basic_info")
    # stock_basic_info:five_days_predict = 1:1
    five_days_predict = relationship("FiveDaysPredict", back_populates="stock_basic_info")
    # stock_basic_info:stock_data = 1:many
    stock_data = relationship('StockData')

    def __init__(self, stock_symbol,  stock_name):
        """建構子"""
        self.stock_symbol = stock_symbol
        self.stock_name = stock_name

    def update_attr(self, attr: dict):
        """動態調整欄位"""
        for key, item in attr.items():
            setattr(self, key, item)
        session.add(self)
        session.commit()

    def append_three_days_predict_data(self, three_days_predict_data):
        """依靠relationship add three_days_predict_data_data"""
        self.three_days_predict.append(three_days_predict_data)
        session.add(self)
        session.commit()

    def append_five_days_predict_data(self, five_days_predict_data):
        """依靠relationship add five_days_predict_data_data"""
        self.five_days_predict.append(five_days_predict_data)
        session.add(self)
        session.commit()

    @classmethod
    def create(cls, **kwargs):
        """新增"""
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj
