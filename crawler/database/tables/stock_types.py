from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from crawler.database import Base, session


class StockTypes(Base):
    """table: 股票類別"""
    __tablename__ = 'stock_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=10), nullable=False, unique=True)
    # relationship
    stock_basic_info = relationship("StockBasicInfo")  # StockTypes:StockBasicInfo = 一:多

    def __init__(self, name):
        """建構子"""
        self.name = name

    def __repr__(self):
        """複印"""
        return "<IndustryTypes(id={}, name={})"\
            .format(self.id, self.name)

    @classmethod
    def get_dict_data(cls):
        data = session.query(cls).all()
        output = {}
        for each_data in data:
            output[each_data.name] = each_data.id
        return output

    @classmethod
    def create(cls, **kwargs):
        """新增"""
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        return obj
