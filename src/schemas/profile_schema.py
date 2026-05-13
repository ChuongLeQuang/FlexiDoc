"""
EN: Pydantic schemas for Profile and Mapping Rules.
VI: Pydantic schemas cho Mẫu cấu hình và Quy tắc ánh xạ.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class MappingRuleBase(BaseModel):
    """Schema cơ sở cho Quy tắc ánh xạ."""

    variable_type: str = Field(description="Loại biến (single hoặc table)")
    word_var: str = Field(description="Tên biến trong file Word")
    excel_col: str = Field(description="Tên cột tương ứng trong Excel")
    format_type: str = Field(default="text", description="Định dạng dữ liệu")


class MappingRuleResponse(MappingRuleBase):
    """Schema phản hồi cho Quy tắc ánh xạ (có kèm ID từ DB)."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class ProfileCreate(BaseModel):
    """Schema đầu vào khi tạo mới một Mẫu cấu hình."""

    name: str = Field(description="Tên gợi nhớ của cấu hình")
    template_filename: str = Field(description="Tên file Word gốc")
    sheet_name: str = Field(description="Tên sheet chứa dữ liệu trong Excel")
    header_row: int = Field(default=1, description="Vị trí dòng tiêu đề")
    grouping_key: Optional[str] = Field(
        default=None, description="Cột dùng để gom nhóm dữ liệu (nếu có)"
    )
    filename_pattern: Optional[str] = Field(
        default=None, description="Quy tắc đặt tên file đầu ra"
    )

    rules: List[MappingRuleBase] = Field(
        description="Danh sách các quy tắc ánh xạ đi kèm"
    )


class ProfileResponse(BaseModel):
    """Schema phản hồi khi lấy thông tin Mẫu cấu hình."""

    id: int
    name: str
    template_filename: str
    sheet_name: str
    header_row: int
    grouping_key: Optional[str]
    filename_pattern: Optional[str]

    rules: List[MappingRuleResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
