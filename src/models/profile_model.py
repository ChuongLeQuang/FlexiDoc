"""
EN: Profile database model.
VI: Mô hình cơ sở dữ liệu cho Profile (Mẫu cấu hình).
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.db import Base


class Profile(Base):
    """
    EN: SQLAlchemy Model for Mapping Profiles.
    VI: Lớp Model SQLAlchemy cho các Mẫu Cấu hình Ánh xạ.
    """

    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    template_filename = Column(String, nullable=False)
    sheet_name = Column(String, nullable=False)
    header_row = Column(Integer, default=1, nullable=False)
    grouping_key = Column(String, nullable=True)
    filename_pattern = Column(String, nullable=True)

    rules = relationship(
        "MappingRule", back_populates="profile", cascade="all, delete-orphan"
    )
