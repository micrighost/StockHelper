from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from crawler.database import Base, session


class StockBasicInfo(Base):
    """table: 股票基本資訊"""
    __tablename__ = 'stock_basic_info'
    stock_symbol = Column(String(length=20), primary_key=True)
    industry_type_id = Column(Integer, ForeignKey('industry_types.id'))
    stock_type_id = Column(Integer, ForeignKey('stock_types.id'))
    stock_name = Column(String(length=45), nullable=False)
    # relationship
    stock_basic_info_detail = relationship("StockBasicInfoDetail", uselist=False, back_populates="stock_basic_info")
    stock_technical_data = relationship("StockTechnicalData")  # StockBasicInfo:StockTechnicalData = 一:多

    def __init__(self, stock_symbol,  stock_name, industry_type_id, stock_type_id):
        """建構子"""
        self.stock_symbol = stock_symbol
        self.stock_name = stock_name
        self.industry_type_id = industry_type_id
        self.stock_type_id = stock_type_id

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
