from AI.database import Base, engine, session
# 引入要新增的table
from AI.database.tables.stock_basic_info import StockBasicInfo
from AI.database.tables.three_days_predict import ThreeDaysPredict
from AI.database.tables.stock_data import StockData
from AI.database.tables.five_days_predict import FiveDaysPredict

if __name__ == '__main__':
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
