from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float
)
from sqlalchemy.orm import relationship
from AI.database import Base, session


class ThreeDaysPredict(Base):
    """table: 股票預測三天後價格"""
    __tablename__ = 'three_days_predict'
    stock_basic_info_id = Column(Integer, ForeignKey('stock_basic_info.id'), primary_key=True)
    three_days_increase_one_percent = Column(Float, nullable=False)
    three_days_increase_three_percent = Column(Float, nullable=False)
    three_days_no_change = Column(Float, nullable=False)
    three_days_decrease_one_percent = Column(Float, nullable=False)
    three_days_decrease_three_percent = Column(Float, nullable=False)
    # relationship
    # stock_basic_info:three_days_predict = 1:1
    stock_basic_info = relationship("StockBasicInfo", back_populates="three_days_predict")

    def __init__(self, **data):
        """建構子"""
        for key, item in data.items():
            setattr(self, key, item)

    def update_attr(self, attr: dict):
        """動態調整欄位"""
        for key, item in attr.items():
            setattr(self, key, item)
        session.add(self)
        session.commit()

    def __repr__(self):
        """複印"""
        return "<StockBasicInfo(id={}, stock_symbol={}, stock_name={}, industry_type_id={}, stock_type_id={})"\
            .format(self.id, self.stock_symbol, self.stock_name, self.industry_type_id, self.stock_type_id)

    def append_stock_technical_data(self, stock_technical_data):
        """依靠relationship add stock_technical_data"""
        self.stock_technical_data.append(stock_technical_data)
        session.add(self)
        session.commit()

    @classmethod
    def create(cls, **kwargs):
        """新增"""
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj
