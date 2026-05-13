"""
EN: Database setup, engine configuration and session management.
VI: Thiết lập cơ sở dữ liệu, cấu hình engine và quản lý phiên.
"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# EN: Ensure 'data' directory exists at the root level for the SQLite file
# VI: Đảm bảo thư mục 'data' tồn tại ở cấp gốc để lưu file SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'flexidoc.sqlite')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db() -> None:
    """
    EN: Initialize the database, creating all tables if they don't exist.
    VI: Khởi tạo cơ sở dữ liệu, tạo tất cả các bảng nếu chúng chưa tồn tại.
    """
    from src.models.profile_model import Profile
    from src.models.mapping_rule import MappingRule

    Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    """
    EN: Dependency to get DB session for FastAPI endpoints.
    VI: Hàm dependency để lấy phiên DB cho các endpoint FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
