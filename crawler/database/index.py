from crawler.database import Base, engine, session
# 引入要新增的table
from crawler.database.tables.industry_types import IndustryTypes
from crawler.database.tables.stock_basic_info import StockBasicInfo
from crawler.database.tables.stock_basic_info_detail import StockBasicInfoDetail
from crawler.database.tables.stock_types import StockTypes
from crawler.database.tables.stock_technical_data import StockTechnicalData
from crawler.database.tables.stock_chip import StockChip

if __name__ == '__main__':
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

