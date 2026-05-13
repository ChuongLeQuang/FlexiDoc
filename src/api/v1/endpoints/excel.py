"""
EN: API endpoints for Excel data validation.
VI: API endpoints kiểm tra và xác thực dữ liệu Excel.
"""

import io
import openpyxl
from fastapi import APIRouter, UploadFile, File, Form
from src.schemas.document import ExcelValidationResponse
from src.services import excel_service

router = APIRouter()


@router.post("/validate", response_model=ExcelValidationResponse)
async def validate_excel(
    file: UploadFile = File(...), sheet_name: str = Form(...), header_row: int = Form(1)
):
    """Kiểm tra tính hợp lệ của file Excel và trích xuất danh sách cột."""
    content = await file.read()
    excel_service.validate_sheet(content, sheet_name)

    # Load tạm thời để lấy danh sách cột và sheets
    wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True, read_only=True)
    sheet_names = wb.sheetnames

    # Openpyxl bắt buộc dùng active mode cho normalize nếu read_only
    headers = excel_service.normalize_headers(wb[sheet_name], header_row)
    wb.close()

    return ExcelValidationResponse(sheet_names=sheet_names, columns=headers)
