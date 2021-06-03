from sqlalchemy import Column, String, ForeignKey, Date, Float, Integer
from sqlalchemy.orm import relationship
from crawler.database import Base, session


class StockTechnicalData(Base):
    """table: 股票技術指標資訊"""
    __tablename__ = 'stock_technical_data'
    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String(length=20), ForeignKey('stock_basic_info.stock_symbol'))
    opening_price = Column(Float, nullable=False)
    closing_price = Column(Float, nullable=False)
    highest_price = Column(Float, nullable=False)
    lowest_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    # def __init__(self, stock_symbol,  opening_price, closing_price, highest_price, lowest_price, volume, date):
    #     """建構子"""
    #     self.stock_symbol = stock_symbol
    #     self.opening_price = opening_price
    #     self.closing_price = closing_price
    #     self.highest_price = highest_price
    #     self.lowest_price = lowest_price
    #     self.volume = volume
    #     self.date = date

    def update_attr(self, attr: dict):
        """動態調整欄位"""
        for key, item in attr.items():
            setattr(self, key, item)
        session.add(self)
        session.commit()

    def __repr__(self):
        """複印"""
        return "<StockTechnicalData(stock_symbol={}, opening_price={}, closing_price={}, highest_price={}), " \
               "lowest_price={}, volume={}"\
            .format(self.stock_symbol, self.opening_price, self.closing_price,
                    self.highest_price, self.volume)

    @classmethod
    def create(cls, **kwargs):
        """新增"""
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj
