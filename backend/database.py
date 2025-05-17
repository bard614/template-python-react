from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import Generator
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 資料庫連線設定
DB_USER = "root"
DB_PASSWORD = "1qaz2wsx"
DB_HOST = "localhost"
DB_PORT = "3307"
DB_NAME = "user_management"

# 建立資料庫連線字串
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 建立資料庫引擎
engine = create_engine(
    DATABASE_URL,
    echo=True  # 啟用 SQL 語句輸出，方便調試
)

# 建立 SessionLocal 類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立 Base 類別
class Base(DeclarativeBase):
    pass

# 取得資料庫連線
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 