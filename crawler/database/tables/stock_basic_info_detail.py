from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from crawler.database import Base, session


class StockBasicInfoDetail(Base):
    """table: 股票基本資訊細項"""
    __tablename__ = 'stock_basic_info_detail'
    stock_symbol = Column(String(length=20), ForeignKey('stock_basic_info.stock_symbol'), primary_key=True)
    company_address = Column(String(length=255))
    company_phone_number = Column(String(length=20))
    business_description = Column(Text)
    establishment_day = Column(Date)
    # relationship
    stock_basic_info = relationship("StockBasicInfo", back_populates="stock_basic_info_detail")

    def __init__(self, stock_symbol, company_address, company_phone_number, business_description, establishment_day):
        """建構子"""
        self.stock_symbol = stock_symbol
        self.company_address = company_address
        self.company_phone_number = company_phone_number
        self.business_description = business_description
        self.establishment_day = establishment_day

    def update_attr(self, attr: dict):
        """動態調整欄位"""
        for key, item in attr.items():
            setattr(self, key, item)
        session.add(self)
        session.commit()

    def __repr__(self):
        """複印"""
        return "<StockBasicInfoDetail(stock_symbol={}, company_address={}, " \
               "company_phone_number={}, business_description={}, establishment_day={}, " \
               "TWSE_listed_day={}, OTC_listed_day={})"\
            .format(self.stock_symbol, self.company_address, self.company_phone_number, self.business_description,
                    self.establishment_day)

    @classmethod
    def create(cls, **kwargs):
        """新增"""
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
