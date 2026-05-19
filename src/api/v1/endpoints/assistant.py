"""
EN: API endpoints for the Assistant Module (Tag Builder).
VI: API endpoints cho Module Trợ lý Sinh Thẻ & Tạo Excel.
"""

from typing import List
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse
from src.services import excel_service

router = APIRouter()


@router.post("/generate-excel")
async def generate_excel(variables: List[str] = Body(...)):
    """Sinh file Excel mẫu rỗng dựa trên danh sách biến."""
    try:
        excel_bytes = excel_service.create_empty_template(variables)
        return StreamingResponse(
            iter([excel_bytes]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=Du_Lieu_Mau.xlsx"},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
