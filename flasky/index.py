import os
from flask_migrate import Migrate
from dotenv import load_dotenv
from app import create_app, db
# 註冊models
from app.models import (
    users,
    stock_basic_info,
    trade_records,
    stock_data,
    stock_chip,
    three_days_predict,
    five_days_predict
)

# 抓取env檔案位置。
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# 若env檔案位置存在，讀取環境變數。
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# 建立Flask的Current App
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# 資料庫遷移腳本
migrate = Migrate(app, db)
