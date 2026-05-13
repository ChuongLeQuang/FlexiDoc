"""
EN: API endpoints for generating final documents.
VI: API endpoints trộn dữ liệu và sinh tài liệu.
"""

import io
import json
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from src.services import excel_service, generator_service

router = APIRouter()


@router.post("/generate")
async def generate_documents(
    word_file: UploadFile = File(...),
    excel_file: UploadFile = File(...),
    sheet_name: str = Form(...),
    header_row: int = Form(1),
    grouping_key: str = Form(None),
    filename_pattern: str = Form("Result_{{id}}"),
    rules: str = Form(...),  # Gửi mảng JSON string do giới hạn của FormData
    filter_col: str = Form(""),
    selected_keys: str = Form("[]"),
):
    """Nhận file và thông số, trộn dữ liệu, sinh hàng loạt Word và nén trả về file ZIP."""
    word_bytes = await word_file.read()
    excel_bytes = await excel_file.read()
    rules_list = json.loads(rules)
    selected_keys_list = json.loads(selected_keys)

    raw_data = excel_service.extract_raw_data(excel_bytes, sheet_name, header_row)

    # Lọc dữ liệu theo đối tượng người dùng đã chọn trên UI

    if selected_keys_list and filter_col:
        raw_data = [
            row
            for row in raw_data
            if str(row.get(filter_col, "")).strip() in selected_keys_list
        ]

    grouped_data = generator_service.group_data_by_key(raw_data, grouping_key)
    zip_bytes = generator_service.render_and_zip(
        word_bytes, grouped_data, rules_list, filename_pattern
    )

    return StreamingResponse(
        io.BytesIO(zip_bytes),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=FlexiDoc_Results.zip"},
    )
