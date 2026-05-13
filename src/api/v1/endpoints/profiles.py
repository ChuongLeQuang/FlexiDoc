"""
EN: API endpoints for CRUD Mapping Profiles.
VI: API endpoints quản lý dữ liệu (CRUD) Mẫu cấu hình ánh xạ.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.database.db import get_db
from src.schemas.profile_schema import ProfileCreate, ProfileResponse
from src.models.profile_model import Profile
from src.models.mapping_rule import MappingRule

router = APIRouter()


@router.get("/", response_model=List[ProfileResponse])
def get_profiles(db: Session = Depends(get_db)):
    """Lấy danh sách tất cả các Mẫu cấu hình (Profiles) đã lưu."""
    profiles = db.query(Profile).all()
    return profiles


@router.post("/", response_model=ProfileResponse)
def create_profile(profile_in: ProfileCreate, db: Session = Depends(get_db)):
    """Tạo và lưu trữ một Mẫu cấu hình cùng các Quy tắc ánh xạ (Mapping Rules) mới."""
    db_profile = Profile(
        name=profile_in.name,
        template_filename=profile_in.template_filename,
        sheet_name=profile_in.sheet_name,
        header_row=profile_in.header_row,
        grouping_key=profile_in.grouping_key,
        filename_pattern=profile_in.filename_pattern,
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    for rule in profile_in.rules:
        db_rule = MappingRule(profile_id=db_profile.id, **rule.model_dump())
        db.add(db_rule)

    db.commit()
    db.refresh(db_profile)
    return db_profile
