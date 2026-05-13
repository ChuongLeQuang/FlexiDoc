"""
EN: Unit tests for Word Service.
VI: Kịch bản kiểm thử cho Dịch vụ Word.
"""

import pytest
import io
import docx
from src.services.word_service import (
    extract_variables,
    preprocess_template,
    validate_syntax,
)
from src.exceptions.custom_errors import (
    InvalidFileFormatError,
    ZeroVariableError,
    TemplateSyntaxError,
)


def create_dummy_docx(text: str) -> bytes:
    """Tạo một file Word ảo trên RAM để test."""
    doc = docx.Document()
    doc.add_paragraph(text)
    out = io.BytesIO()
    doc.save(out)
    return out.getvalue()


def test_extract_variables_zero():
    """Test lỗi khi không có biến nào."""
    template = create_dummy_docx("Đây là file không có biến.")
    with pytest.raises(ZeroVariableError):
        extract_variables(template)


def test_extract_variables_success():
    """Test trích xuất biến đơn và biến bảng thành công."""
    template = create_dummy_docx(
        "Họ tên: {{ ho_ten }}\n"
        "{{ table_start:danh_sach }}\n"
        "STT: {{ stt }} - Lương: {{ item.luong }}\n"
        "{{ table_end }}"
    )
    result = extract_variables(template)
    assert "ho_ten" in result["single_vars"]
    assert "danh_sach" in result["table_vars"]
    assert "stt" in result["table_vars"]["danh_sach"]
    assert "luong" in result["table_vars"]["danh_sach"]


def test_validate_syntax_error():
    """Test bắt lỗi sai cú pháp thẻ Jinja2 (thiếu dấu ngoặc)."""
    # Cố tình viết sai cú pháp (thiếu % ở cuối)
    # Tuy nhiên, docxtpl sử dụng {{ }} nên ta mô phỏng một thẻ if bị sai
    template = create_dummy_docx("Lương là: {% if luong > 1000 %} Cao {% endif")

    with pytest.raises(TemplateSyntaxError):
        validate_syntax(template)
