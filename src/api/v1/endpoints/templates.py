"""
EN: API endpoints for Word template validation.
VI: API endpoints kiểm tra và xác thực mẫu Word.
"""

from fastapi import APIRouter, UploadFile, File
from src.schemas.document import TemplateValidationResponse
from src.services import word_service

router = APIRouter()


@router.post("/validate", response_model=TemplateValidationResponse)
async def validate_template(file: UploadFile = File(...)):
    """Nhận file Word, kiểm tra Jinja2 syntax và trích xuất danh sách biến."""
    content = await file.read()

    word_service.validate_syntax(content)
    vars_dict = word_service.extract_variables(content)

    return TemplateValidationResponse(
        single_vars=vars_dict["single_vars"], table_vars=vars_dict["table_vars"]
    )
