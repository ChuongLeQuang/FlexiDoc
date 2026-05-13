"""
EN: Pydantic schemas for Document Generation and Validation.
VI: Pydantic schemas cho việc Validate và Sinh tài liệu.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class TemplateValidationResponse(BaseModel):
    """Schema phản hồi khi phân tích thành công Mẫu Word."""

    single_vars: List[str] = Field(description="Danh sách các biến đơn")
    table_vars: Dict[str, List[str]] = Field(
        description="Danh sách các biến bảng biểu, gom nhóm theo tên bảng"
    )


class ExcelValidationResponse(BaseModel):
    """Schema phản hồi khi phân tích thành công file Excel."""

    sheet_names: List[str] = Field(description="Danh sách các sheet có trong file")
    columns: List[str] = Field(description="Danh sách tên các cột của sheet được chọn")


class GeneratePayload(BaseModel):
    """
    Schema chứa dữ liệu cấu hình sinh tài liệu.
    Lưu ý: File sẽ được gửi qua form-data thay vì JSON body.
    """

    filename_pattern: str = Field(
        default="Result_{{id}}", description="Cấu hình quy tắc đặt tên file Word đầu ra"
    )
    # Payload bổ sung sẽ được mở rộng khi nối API thực tế
