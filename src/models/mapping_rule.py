"""
EN: MappingRule database model.
VI: Mô hình cơ sở dữ liệu cho MappingRule (Quy tắc ánh xạ).
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base


class MappingRule(Base):
    """
    EN: SQLAlchemy Model for Mapping Rules corresponding to a Profile.
    VI: Lớp Model SQLAlchemy cho các Quy tắc Ánh xạ thuộc về một Mẫu cấu hình.
    """

    __tablename__ = "mapping_rules"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    variable_type = Column(String, nullable=False)
    word_var = Column(String, nullable=False)
    excel_col = Column(String, nullable=False)
    format_type = Column(String, default="text")

    profile = relationship("Profile", back_populates="rules")
