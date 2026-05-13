"""
EN: Main router aggregator for API v1.
VI: Khối gom nhóm router chính cho API v1.
"""

from fastapi import APIRouter
from src.api.v1.endpoints import templates, excel, profiles, documents

api_router = APIRouter()

# Gắn (Include) các router con
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(excel.router, prefix="/excel", tags=["excel"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
