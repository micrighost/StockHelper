from sqlalchemy import Column, Integer, String, Date
from crawler.database import Base, session


class StockChip(Base):
    """table: 三大法人籌碼"""
    __tablename__ = 'stock_chip'
    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String(length=20))
    net_buy_volume = Column(Integer)
    date = Column(Date, nullable=False)

    @classmethod
    def create(cls, **kwargs):
        """新增"""
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
